"""
Comprehensive Database Management for Synthetic Ascension
Handles SQL, vector, cache, and document databases with enterprise-grade features
"""

import os
import json
import chromadb
from chromadb.config import Settings
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime, timedelta
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    """
    Centralized database management for all storage types:
    - PostgreSQL (relational data)
    - ChromaDB (vector embeddings for literature and medical concepts)
    - In-memory cache (session data and temporary results)
    - JSON document store (configuration and metadata)
    """
    
    def __init__(self):
        self.chroma_client = None
        self.cache = {}
        self.document_store = {}
        self.collections = {}
        self._initialize_databases()
    
    def _initialize_databases(self):
        """Initialize all database connections"""
        try:
            # Initialize ChromaDB for vector storage
            self.chroma_client = chromadb.PersistentClient(
                path="./vector_db",
                settings=Settings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )
            
            # Create essential collections
            self._create_vector_collections()
            
            # Initialize document store
            self._initialize_document_store()
            
            logger.info("All databases initialized successfully")
            
        except Exception as e:
            logger.error(f"Database initialization error: {e}")
            raise
    
    def _create_vector_collections(self):
        """Create ChromaDB collections for different data types"""
        try:
            # Medical literature embeddings
            self.collections['literature'] = self.chroma_client.get_or_create_collection(
                name="medical_literature",
                metadata={"description": "PubMed articles and medical research embeddings"}
            )
            
            # Clinical concepts and terminologies
            self.collections['clinical_concepts'] = self.chroma_client.get_or_create_collection(
                name="clinical_concepts", 
                metadata={"description": "Medical terminologies, ICD codes, drug concepts"}
            )
            
            # Patient cohort similarity vectors
            self.collections['patient_vectors'] = self.chroma_client.get_or_create_collection(
                name="patient_similarity",
                metadata={"description": "Patient feature vectors for similarity matching"}
            )
            
            # Biomedical knowledge graph embeddings
            self.collections['knowledge_graph'] = self.chroma_client.get_or_create_collection(
                name="biomedical_kg",
                metadata={"description": "Biomedical knowledge graph entity embeddings"}
            )
            
            logger.info("Vector collections created successfully")
            
        except Exception as e:
            logger.error(f"Error creating vector collections: {e}")
            raise
    
    def _initialize_document_store(self):
        """Initialize JSON document store for configurations and metadata"""
        self.document_store = {
            'system_config': {
                'version': '1.0.0',
                'last_updated': datetime.now().isoformat(),
                'features': {
                    'vector_search': True,
                    'literature_integration': True,
                    'real_time_updates': True
                }
            },
            'user_sessions': {},
            'agent_metadata': {},
            'workflow_templates': {},
            'validation_schemas': {}
        }
    
    # Vector Database Operations
    def add_literature_embeddings(self, documents: List[Dict[str, Any]]) -> bool:
        """Add medical literature embeddings to vector database"""
        try:
            if not documents:
                return False
                
            ids = [doc.get('id', str(uuid.uuid4())) for doc in documents]
            embeddings = [doc['embedding'] for doc in documents if 'embedding' in doc]
            metadatas = [doc.get('metadata', {}) for doc in documents]
            documents_text = [doc.get('text', '') for doc in documents]
            
            if embeddings:
                self.collections['literature'].add(
                    embeddings=embeddings,
                    metadatas=metadatas,
                    documents=documents_text,
                    ids=ids
                )
                logger.info(f"Added {len(embeddings)} literature embeddings")
                return True
            return False
            
        except Exception as e:
            logger.error(f"Error adding literature embeddings: {e}")
            return False
    
    def search_similar_literature(self, query_embedding: List[float], n_results: int = 10) -> List[Dict]:
        """Search for similar medical literature using vector similarity"""
        try:
            results = self.collections['literature'].query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                include=['metadatas', 'documents', 'distances']
            )
            
            formatted_results = []
            if results['metadatas'] and results['metadatas'][0]:
                for i, metadata in enumerate(results['metadatas'][0]):
                    formatted_results.append({
                        'metadata': metadata,
                        'document': results['documents'][0][i] if results['documents'] else '',
                        'similarity': 1 - results['distances'][0][i] if results['distances'] else 0
                    })
            
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error searching literature: {e}")
            return []
    
    def add_clinical_concepts(self, concepts: List[Dict[str, Any]]) -> bool:
        """Add clinical concept embeddings"""
        try:
            if not concepts:
                return False
                
            ids = [concept.get('id', str(uuid.uuid4())) for concept in concepts]
            embeddings = [concept['embedding'] for concept in concepts if 'embedding' in concept]
            metadatas = [concept.get('metadata', {}) for concept in concepts]
            documents_text = [concept.get('text', '') for concept in concepts]
            
            if embeddings:
                self.collections['clinical_concepts'].add(
                    embeddings=embeddings,
                    metadatas=metadatas,
                    documents=documents_text,
                    ids=ids
                )
                logger.info(f"Added {len(embeddings)} clinical concept embeddings")
                return True
            return False
            
        except Exception as e:
            logger.error(f"Error adding clinical concepts: {e}")
            return False
    
    def add_patient_vectors(self, patient_data: List[Dict[str, Any]]) -> bool:
        """Add patient feature vectors for similarity analysis"""
        try:
            if not patient_data:
                return False
                
            ids = [p.get('patient_id', str(uuid.uuid4())) for p in patient_data]
            embeddings = [p['features'] for p in patient_data if 'features' in p]
            metadatas = [p.get('metadata', {}) for p in patient_data]
            documents_text = [json.dumps(p.get('summary', {})) for p in patient_data]
            
            if embeddings:
                self.collections['patient_vectors'].add(
                    embeddings=embeddings,
                    metadatas=metadatas,
                    documents=documents_text,
                    ids=ids
                )
                logger.info(f"Added {len(embeddings)} patient vectors")
                return True
            return False
            
        except Exception as e:
            logger.error(f"Error adding patient vectors: {e}")
            return False
    
    def find_similar_patients(self, patient_features: List[float], n_results: int = 5) -> List[Dict]:
        """Find similar patients based on feature vectors"""
        try:
            results = self.collections['patient_vectors'].query(
                query_embeddings=[patient_features],
                n_results=n_results,
                include=['metadatas', 'documents', 'distances']
            )
            
            similar_patients = []
            if results['metadatas'] and results['metadatas'][0]:
                for i, metadata in enumerate(results['metadatas'][0]):
                    similar_patients.append({
                        'patient_metadata': metadata,
                        'summary': json.loads(results['documents'][0][i]) if results['documents'] else {},
                        'similarity_score': 1 - results['distances'][0][i] if results['distances'] else 0
                    })
            
            return similar_patients
            
        except Exception as e:
            logger.error(f"Error finding similar patients: {e}")
            return []
    
    # Cache Operations
    def cache_set(self, key: str, value: Any, ttl_seconds: int = 3600) -> bool:
        """Set cache value with TTL"""
        try:
            expiry = datetime.now() + timedelta(seconds=ttl_seconds)
            self.cache[key] = {
                'value': value,
                'expiry': expiry
            }
            return True
        except Exception as e:
            logger.error(f"Error setting cache: {e}")
            return False
    
    def cache_get(self, key: str) -> Optional[Any]:
        """Get cache value if not expired"""
        try:
            if key not in self.cache:
                return None
                
            cached_item = self.cache[key]
            if datetime.now() > cached_item['expiry']:
                del self.cache[key]
                return None
                
            return cached_item['value']
        except Exception as e:
            logger.error(f"Error getting cache: {e}")
            return None
    
    def cache_delete(self, key: str) -> bool:
        """Delete cache entry"""
        try:
            if key in self.cache:
                del self.cache[key]
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting cache: {e}")
            return False
    
    def cache_clear_expired(self) -> int:
        """Clear expired cache entries"""
        try:
            now = datetime.now()
            expired_keys = [
                key for key, value in self.cache.items() 
                if now > value['expiry']
            ]
            
            for key in expired_keys:
                del self.cache[key]
                
            logger.info(f"Cleared {len(expired_keys)} expired cache entries")
            return len(expired_keys)
        except Exception as e:
            logger.error(f"Error clearing expired cache: {e}")
            return 0
    
    # Document Store Operations
    def doc_store_set(self, collection: str, doc_id: str, document: Dict[str, Any]) -> bool:
        """Store document in collection"""
        try:
            if collection not in self.document_store:
                self.document_store[collection] = {}
                
            self.document_store[collection][doc_id] = {
                'data': document,
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
            return True
        except Exception as e:
            logger.error(f"Error storing document: {e}")
            return False
    
    def doc_store_get(self, collection: str, doc_id: str) -> Optional[Dict[str, Any]]:
        """Get document from collection"""
        try:
            if collection in self.document_store and doc_id in self.document_store[collection]:
                return self.document_store[collection][doc_id]['data']
            return None
        except Exception as e:
            logger.error(f"Error getting document: {e}")
            return None
    
    def doc_store_list(self, collection: str) -> List[str]:
        """List all document IDs in collection"""
        try:
            if collection in self.document_store:
                return list(self.document_store[collection].keys())
            return []
        except Exception as e:
            logger.error(f"Error listing documents: {e}")
            return []
    
    def doc_store_delete(self, collection: str, doc_id: str) -> bool:
        """Delete document from collection"""
        try:
            if collection in self.document_store and doc_id in self.document_store[collection]:
                del self.document_store[collection][doc_id]
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting document: {e}")
            return False
    
    # Health Check Operations
    def health_check(self) -> Dict[str, Any]:
        """Comprehensive health check for all database systems"""
        try:
            health_status = {
                'timestamp': datetime.now().isoformat(),
                'overall_status': 'healthy',
                'components': {}
            }
            
            # Vector database health
            try:
                collection_count = len(self.collections)
                total_items = sum([
                    col.count() for col in self.collections.values()
                ])
                health_status['components']['vector_db'] = {
                    'status': 'healthy',
                    'collections': collection_count,
                    'total_items': total_items
                }
            except Exception as e:
                health_status['components']['vector_db'] = {
                    'status': 'unhealthy',
                    'error': str(e)
                }
                health_status['overall_status'] = 'degraded'
            
            # Cache health
            try:
                expired_count = self.cache_clear_expired()
                health_status['components']['cache'] = {
                    'status': 'healthy',
                    'active_entries': len(self.cache),
                    'expired_cleared': expired_count
                }
            except Exception as e:
                health_status['components']['cache'] = {
                    'status': 'unhealthy',
                    'error': str(e)
                }
                health_status['overall_status'] = 'degraded'
            
            # Document store health
            try:
                collection_count = len(self.document_store)
                total_docs = sum([
                    len(docs) for docs in self.document_store.values()
                ])
                health_status['components']['document_store'] = {
                    'status': 'healthy',
                    'collections': collection_count,
                    'total_documents': total_docs
                }
            except Exception as e:
                health_status['components']['document_store'] = {
                    'status': 'unhealthy',
                    'error': str(e)
                }
                health_status['overall_status'] = 'degraded'
            
            return health_status
            
        except Exception as e:
            logger.error(f"Error in health check: {e}")
            return {
                'timestamp': datetime.now().isoformat(),
                'overall_status': 'unhealthy',
                'error': str(e)
            }
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get comprehensive database statistics"""
        try:
            stats = {
                'vector_database': {
                    'collections': len(self.collections),
                    'collection_details': {}
                },
                'cache': {
                    'active_entries': len(self.cache),
                    'memory_usage_estimate': sum([
                        len(str(item)) for item in self.cache.values()
                    ])
                },
                'document_store': {
                    'collections': len(self.document_store),
                    'total_documents': sum([
                        len(docs) for docs in self.document_store.values()
                    ])
                }
            }
            
            # Detailed vector collection stats
            for name, collection in self.collections.items():
                try:
                    stats['vector_database']['collection_details'][name] = {
                        'item_count': collection.count(),
                        'metadata': collection.metadata
                    }
                except Exception as e:
                    stats['vector_database']['collection_details'][name] = {
                        'error': str(e)
                    }
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting database stats: {e}")
            return {'error': str(e)}

# Global database manager instance
db_manager = DatabaseManager()

def get_database_manager() -> DatabaseManager:
    """Get the global database manager instance"""
    return db_manager