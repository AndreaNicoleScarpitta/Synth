"""
Security utilities for Synthetic Ascension API
Implements JWT authentication, API key management, and access control
"""

import jwt
import hashlib
import secrets
import bcrypt
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Any
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
import json
from enum import Enum

# Security configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", secrets.token_urlsafe(32))
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
API_KEY_EXPIRE_DAYS = 365

security = HTTPBearer()

class UserRole(str, Enum):
    """User role enumeration for access control"""
    ADMIN = "admin"
    RESEARCHER = "researcher"
    ANALYST = "analyst"
    VIEWER = "viewer"

class AccessLevel(str, Enum):
    """Data access level enumeration"""
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"

# Role-based permissions mapping
ROLE_PERMISSIONS = {
    UserRole.ADMIN: {
        "biomedical_search": [AccessLevel.PUBLIC, AccessLevel.INTERNAL, AccessLevel.CONFIDENTIAL, AccessLevel.RESTRICTED],
        "cohort_generation": [AccessLevel.PUBLIC, AccessLevel.INTERNAL, AccessLevel.CONFIDENTIAL, AccessLevel.RESTRICTED],
        "data_export": [AccessLevel.PUBLIC, AccessLevel.INTERNAL, AccessLevel.CONFIDENTIAL],
        "user_management": [AccessLevel.PUBLIC, AccessLevel.INTERNAL, AccessLevel.CONFIDENTIAL, AccessLevel.RESTRICTED],
        "audit_logs": [AccessLevel.PUBLIC, AccessLevel.INTERNAL, AccessLevel.CONFIDENTIAL, AccessLevel.RESTRICTED]
    },
    UserRole.RESEARCHER: {
        "biomedical_search": [AccessLevel.PUBLIC, AccessLevel.INTERNAL, AccessLevel.CONFIDENTIAL],
        "cohort_generation": [AccessLevel.PUBLIC, AccessLevel.INTERNAL, AccessLevel.CONFIDENTIAL],
        "data_export": [AccessLevel.PUBLIC, AccessLevel.INTERNAL],
        "user_management": [],
        "audit_logs": [AccessLevel.PUBLIC]
    },
    UserRole.ANALYST: {
        "biomedical_search": [AccessLevel.PUBLIC, AccessLevel.INTERNAL],
        "cohort_generation": [AccessLevel.PUBLIC, AccessLevel.INTERNAL],
        "data_export": [AccessLevel.PUBLIC],
        "user_management": [],
        "audit_logs": [AccessLevel.PUBLIC]
    },
    UserRole.VIEWER: {
        "biomedical_search": [AccessLevel.PUBLIC],
        "cohort_generation": [],
        "data_export": [],
        "user_management": [],
        "audit_logs": []
    }
}

class SecurityManager:
    """Centralized security management for API endpoints"""
    
    def __init__(self):
        self.api_keys = {}  # In production, use a secure database
        self.revoked_tokens = set()  # In production, use Redis or database
        self.rate_limits = {}  # Rate limiting storage
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire, "iat": datetime.utcnow()})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify and decode JWT token"""
        try:
            if token in self.revoked_tokens:
                return None
            
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            
            # Check if token is expired
            exp = payload.get("exp")
            if exp and datetime.utcnow() > datetime.fromtimestamp(exp):
                return None
            
            return payload
        except jwt.PyJWTError:
            return None
    
    def generate_api_key(self, user_id: str, role: UserRole, description: str = "") -> str:
        """Generate new API key"""
        api_key = f"sa_{secrets.token_urlsafe(32)}"
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()
        
        self.api_keys[key_hash] = {
            "user_id": user_id,
            "role": role,
            "description": description,
            "created_at": datetime.utcnow().isoformat(),
            "last_used": None,
            "usage_count": 0,
            "expires_at": (datetime.utcnow() + timedelta(days=API_KEY_EXPIRE_DAYS)).isoformat()
        }
        
        return api_key
    
    def verify_api_key(self, api_key: str) -> Optional[Dict[str, Any]]:
        """Verify API key and return associated data"""
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()
        key_data = self.api_keys.get(key_hash)
        
        if not key_data:
            return None
        
        # Check expiration
        expires_at = datetime.fromisoformat(key_data["expires_at"])
        if datetime.utcnow() > expires_at:
            return None
        
        # Update usage statistics
        key_data["last_used"] = datetime.utcnow().isoformat()
        key_data["usage_count"] += 1
        
        return key_data
    
    def revoke_token(self, token: str):
        """Revoke a JWT token"""
        self.revoked_tokens.add(token)
    
    def revoke_api_key(self, api_key: str) -> bool:
        """Revoke an API key"""
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()
        if key_hash in self.api_keys:
            del self.api_keys[key_hash]
            return True
        return False
    
    def check_rate_limit(self, identifier: str, limit: int, window_minutes: int = 60) -> bool:
        """Check if request is within rate limits"""
        now = datetime.utcnow()
        window_start = now - timedelta(minutes=window_minutes)
        
        if identifier not in self.rate_limits:
            self.rate_limits[identifier] = []
        
        # Remove old requests outside the window
        self.rate_limits[identifier] = [
            req_time for req_time in self.rate_limits[identifier]
            if req_time > window_start
        ]
        
        # Check if under limit
        if len(self.rate_limits[identifier]) >= limit:
            return False
        
        # Add current request
        self.rate_limits[identifier].append(now)
        return True
    
    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

# Global security manager instance
security_manager = SecurityManager()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """Dependency to get current authenticated user from JWT token"""
    token = credentials.credentials
    payload = security_manager.verify_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return payload

def get_current_user_api_key(api_key: str) -> Dict[str, Any]:
    """Get current user from API key"""
    key_data = security_manager.verify_api_key(api_key)
    
    if key_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )
    
    return key_data

def require_role(required_roles: List[UserRole]):
    """Decorator factory for role-based access control"""
    def role_checker(current_user: Dict[str, Any] = Depends(get_current_user)):
        user_role = current_user.get("role")
        if user_role not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required roles: {required_roles}"
            )
        return current_user
    return role_checker

def require_permission(resource: str, access_level: AccessLevel):
    """Decorator factory for permission-based access control"""
    def permission_checker(current_user: Dict[str, Any] = Depends(get_current_user)):
        user_role = UserRole(current_user.get("role"))
        
        if resource not in ROLE_PERMISSIONS.get(user_role, {}):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"No access to resource: {resource}"
            )
        
        allowed_levels = ROLE_PERMISSIONS[user_role][resource]
        if access_level not in allowed_levels:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient access level for {resource}. Required: {access_level}"
            )
        
        return current_user
    return permission_checker

def rate_limit(requests_per_hour: int = 100):
    """Rate limiting decorator factory"""
    def rate_limiter(current_user: Dict[str, Any] = Depends(get_current_user)):
        user_id = current_user.get("user_id", "anonymous")
        
        if not security_manager.check_rate_limit(
            identifier=f"user_{user_id}",
            limit=requests_per_hour,
            window_minutes=60
        ):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded. Maximum {requests_per_hour} requests per hour."
            )
        
        return current_user
    return rate_limiter

class DataClassification:
    """Data classification utility for research data"""
    
    @staticmethod
    def classify_biomedical_data(data_type: str, content: str) -> AccessLevel:
        """Classify biomedical data based on sensitivity"""
        
        # Keywords that indicate different sensitivity levels
        restricted_keywords = [
            "patient identification", "personal health information", "phi",
            "social security", "medical record number", "mrn"
        ]
        
        confidential_keywords = [
            "clinical trial participant", "unpublished data", "proprietary",
            "genetic sequence", "genomic data", "biomarker"
        ]
        
        internal_keywords = [
            "institutional data", "internal study", "preliminary results",
            "draft analysis", "pre-publication"
        ]
        
        content_lower = content.lower()
        
        # Check for restricted content
        if any(keyword in content_lower for keyword in restricted_keywords):
            return AccessLevel.RESTRICTED
        
        # Check for confidential content
        if any(keyword in content_lower for keyword in confidential_keywords):
            return AccessLevel.CONFIDENTIAL
        
        # Check for internal content
        if any(keyword in content_lower for keyword in internal_keywords):
            return AccessLevel.INTERNAL
        
        # Default to public for published research
        return AccessLevel.PUBLIC

def audit_log(action: str, resource: str, access_level: AccessLevel):
    """Decorator factory for audit logging"""
    def audit_decorator(func):
        def wrapper(*args, **kwargs):
            # Get current user from kwargs or dependencies
            current_user = None
            for arg in args:
                if isinstance(arg, dict) and "user_id" in arg:
                    current_user = arg
                    break
            
            # Log the access attempt
            log_entry = {
                "timestamp": datetime.utcnow().isoformat(),
                "user_id": current_user.get("user_id") if current_user else "unknown",
                "action": action,
                "resource": resource,
                "access_level": access_level.value,
                "success": True,
                "details": {}
            }
            
            try:
                result = func(*args, **kwargs)
                # In production, save to audit database
                print(f"AUDIT: {json.dumps(log_entry)}")
                return result
            except Exception as e:
                log_entry["success"] = False
                log_entry["error"] = str(e)
                print(f"AUDIT: {json.dumps(log_entry)}")
                raise
        
        return wrapper
    return audit_decorator

# Data encryption utilities
class DataEncryption:
    """Utilities for encrypting sensitive research data"""
    
    @staticmethod
    def encrypt_sensitive_fields(data: Dict[str, Any], sensitive_fields: List[str]) -> Dict[str, Any]:
        """Encrypt specified sensitive fields in data"""
        encrypted_data = data.copy()
        
        for field in sensitive_fields:
            if field in encrypted_data:
                # In production, use proper encryption like Fernet
                value = str(encrypted_data[field])
                encrypted_value = hashlib.sha256(value.encode()).hexdigest()[:16] + "***"
                encrypted_data[field] = encrypted_value
        
        return encrypted_data
    
    @staticmethod
    def redact_pii(text: str) -> str:
        """Redact potential PII from text content"""
        import re
        
        # Redact potential SSNs
        text = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '[SSN-REDACTED]', text)
        
        # Redact potential phone numbers
        text = re.sub(r'\b\d{3}-\d{3}-\d{4}\b', '[PHONE-REDACTED]', text)
        
        # Redact potential email addresses
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL-REDACTED]', text)
        
        # Redact potential medical record numbers
        text = re.sub(r'\bMRN\s*:?\s*\d+\b', '[MRN-REDACTED]', text, flags=re.IGNORECASE)
        
        return text

# Export utilities
def secure_export_headers(access_level: AccessLevel) -> Dict[str, str]:
    """Generate secure headers for data export"""
    headers = {
        "Content-Type": "application/json",
        "X-Data-Classification": access_level.value,
        "X-Export-Timestamp": datetime.utcnow().isoformat(),
        "Cache-Control": "no-cache, no-store, must-revalidate",
        "Pragma": "no-cache",
        "Expires": "0"
    }
    
    if access_level in [AccessLevel.CONFIDENTIAL, AccessLevel.RESTRICTED]:
        headers["X-Content-Type-Options"] = "nosniff"
        headers["X-Frame-Options"] = "DENY"
        headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    
    return headers