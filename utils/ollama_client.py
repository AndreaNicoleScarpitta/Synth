import requests
import json
from typing import Dict, Any, Optional, List
import os
import time

class OllamaClient:
    """Client for interacting with Ollama local LLM server"""
    
    def __init__(self, base_url: str = None, model_name: str = "mistral:latest"):
        self.base_url = base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.model_name = model_name
        self.default_timeout = 120  # 2 minutes timeout for generation
        
        # Generation parameters
        self.default_options = {
            "temperature": 0.7,
            "top_p": 0.9,
            "top_k": 40,
            "num_predict": 2048,
            "num_ctx": 4096,
            "repeat_penalty": 1.1,
            "stop": []
        }
    
    def check_connection(self) -> bool:
        """Check if Ollama server is accessible"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=10)
            return response.status_code == 200
        except Exception as e:
            print(f"Ollama connection check failed: {e}")
            return False
    
    def list_models(self) -> List[Dict[str, Any]]:
        """List available models"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return data.get("models", [])
            
        except Exception as e:
            print(f"Error listing models: {e}")
            return []
    
    def pull_model(self, model_name: str) -> bool:
        """Pull a model from Ollama registry"""
        try:
            url = f"{self.base_url}/api/pull"
            payload = {"name": model_name}
            
            response = requests.post(url, json=payload, timeout=300)  # 5 minute timeout for pull
            response.raise_for_status()
            
            # Stream the response to show progress
            for line in response.iter_lines():
                if line:
                    data = json.loads(line)
                    if "status" in data:
                        print(f"Pull status: {data['status']}")
                    if data.get("status") == "success":
                        return True
            
            return True
            
        except Exception as e:
            print(f"Error pulling model {model_name}: {e}")
            return False
    
    def generate_text(self, prompt: str, model: Optional[str] = None, 
                     options: Optional[Dict[str, Any]] = None, 
                     system_prompt: Optional[str] = None) -> str:
        """
        Generate text using Ollama
        
        Args:
            prompt: The text prompt
            model: Model name (uses default if None)
            options: Generation options
            system_prompt: Optional system prompt
            
        Returns:
            Generated text
        """
        model = model or self.model_name
        options = options or self.default_options.copy()
        
        try:
            # Prepare the request payload
            payload = {
                "model": model,
                "prompt": prompt,
                "options": options,
                "stream": False
            }
            
            if system_prompt:
                payload["system"] = system_prompt
            
            # Make the request
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=self.default_timeout
            )
            response.raise_for_status()
            
            # Parse response
            data = response.json()
            return data.get("response", "")
            
        except requests.exceptions.Timeout:
            error_msg = f"Request timed out after {self.default_timeout} seconds"
            print(error_msg)
            return f"Error: {error_msg}"
        except requests.exceptions.RequestException as e:
            error_msg = f"Request failed: {e}"
            print(error_msg)
            return f"Error: {error_msg}"
        except json.JSONDecodeError as e:
            error_msg = f"Failed to parse response: {e}"
            print(error_msg)
            return f"Error: {error_msg}"
        except Exception as e:
            error_msg = f"Unexpected error: {e}"
            print(error_msg)
            return f"Error: {error_msg}"
    
    def generate_streaming(self, prompt: str, model: Optional[str] = None,
                          options: Optional[Dict[str, Any]] = None,
                          system_prompt: Optional[str] = None):
        """
        Generate text with streaming response
        
        Args:
            prompt: The text prompt
            model: Model name (uses default if None)
            options: Generation options
            system_prompt: Optional system prompt
            
        Yields:
            Chunks of generated text
        """
        model = model or self.model_name
        options = options or self.default_options.copy()
        
        try:
            payload = {
                "model": model,
                "prompt": prompt,
                "options": options,
                "stream": True
            }
            
            if system_prompt:
                payload["system"] = system_prompt
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                stream=True,
                timeout=self.default_timeout
            )
            response.raise_for_status()
            
            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line)
                        if "response" in data:
                            yield data["response"]
                        if data.get("done", False):
                            break
                    except json.JSONDecodeError:
                        continue
                        
        except Exception as e:
            print(f"Error in streaming generation: {e}")
            yield f"Error: {e}"
    
    def chat(self, messages: List[Dict[str, str]], model: Optional[str] = None,
             options: Optional[Dict[str, Any]] = None) -> str:
        """
        Chat using the chat API
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            model: Model name (uses default if None)
            options: Generation options
            
        Returns:
            Assistant's response
        """
        model = model or self.model_name
        options = options or self.default_options.copy()
        
        try:
            payload = {
                "model": model,
                "messages": messages,
                "options": options,
                "stream": False
            }
            
            response = requests.post(
                f"{self.base_url}/api/chat",
                json=payload,
                timeout=self.default_timeout
            )
            response.raise_for_status()
            
            data = response.json()
            message = data.get("message", {})
            return message.get("content", "")
            
        except Exception as e:
            print(f"Error in chat: {e}")
            return f"Error: {e}"
    
    def embed_text(self, text: str, model: Optional[str] = None) -> List[float]:
        """
        Generate embeddings for text
        
        Args:
            text: Text to embed
            model: Model name for embeddings
            
        Returns:
            List of embedding values
        """
        embed_model = model or "nomic-embed-text:latest"
        
        try:
            payload = {
                "model": embed_model,
                "prompt": text
            }
            
            response = requests.post(
                f"{self.base_url}/api/embeddings",
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            
            data = response.json()
            return data.get("embedding", [])
            
        except Exception as e:
            print(f"Error generating embeddings: {e}")
            return []
    
    def get_model_info(self, model_name: str) -> Dict[str, Any]:
        """Get information about a specific model"""
        try:
            payload = {"name": model_name}
            response = requests.post(
                f"{self.base_url}/api/show",
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            print(f"Error getting model info: {e}")
            return {}
    
    def delete_model(self, model_name: str) -> bool:
        """Delete a model from Ollama"""
        try:
            payload = {"name": model_name}
            response = requests.delete(
                f"{self.base_url}/api/delete",
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            return True
            
        except Exception as e:
            print(f"Error deleting model: {e}")
            return False
    
    def health_check(self) -> Dict[str, Any]:
        """Perform a comprehensive health check"""
        health_status = {
            "server_accessible": False,
            "models_available": [],
            "default_model_ready": False,
            "generation_test": False,
            "timestamp": time.time()
        }
        
        try:
            # Check server accessibility
            health_status["server_accessible"] = self.check_connection()
            
            if health_status["server_accessible"]:
                # Check available models
                models = self.list_models()
                health_status["models_available"] = [m.get("name", "") for m in models]
                
                # Check if default model is available
                model_names = health_status["models_available"]
                health_status["default_model_ready"] = self.model_name in model_names
                
                # Test generation if default model is ready
                if health_status["default_model_ready"]:
                    test_response = self.generate_text("Hello", options={"num_predict": 10})
                    health_status["generation_test"] = len(test_response) > 0 and "Error:" not in test_response
        
        except Exception as e:
            health_status["error"] = str(e)
        
        return health_status
    
    def ensure_model_available(self, model_name: str = None) -> bool:
        """Ensure a model is available, pulling it if necessary"""
        model_name = model_name or self.model_name
        
        try:
            # Check if model exists
            models = self.list_models()
            available_models = [m.get("name", "") for m in models]
            
            if model_name in available_models:
                return True
            
            # Try to pull the model
            print(f"Model {model_name} not found, attempting to pull...")
            return self.pull_model(model_name)
            
        except Exception as e:
            print(f"Error ensuring model availability: {e}")
            return False
    
    def optimize_for_medical_domain(self) -> Dict[str, Any]:
        """Optimize generation parameters for medical/biomedical text"""
        medical_options = {
            "temperature": 0.3,  # Lower temperature for more consistent medical text
            "top_p": 0.8,
            "top_k": 20,
            "num_predict": 4096,  # Longer responses for detailed medical content
            "num_ctx": 8192,  # Larger context for medical documents
            "repeat_penalty": 1.2,  # Reduce repetition in medical text
            "stop": ["Patient:", "PATIENT:", "Note:", "NOTE:"]  # Medical document stops
        }
        
        self.default_options.update(medical_options)
        return medical_options
    
    def create_medical_system_prompt(self) -> str:
        """Create a system prompt optimized for medical/biomedical content"""
        return """You are a medical AI assistant with expertise in biomedical research, clinical practice, and health informatics. 

Your responses should be:
- Accurate and evidence-based
- Professional and appropriate for healthcare contexts
- Mindful of patient privacy and medical ethics
- Clear and well-structured
- Based on current medical knowledge and best practices

When generating synthetic medical content:
- Ensure clinical realism and plausibility
- Follow medical terminology and formatting standards
- Maintain consistency with medical guidelines
- Avoid any real patient information or identifiers

Always prioritize safety, accuracy, and ethical considerations in medical contexts."""

# Example usage and testing functions
def test_ollama_connection():
    """Test function to verify Ollama connection and capabilities"""
    client = OllamaClient()
    
    print("Testing Ollama connection...")
    health = client.health_check()
    
    print(f"Server accessible: {health['server_accessible']}")
    print(f"Available models: {health['models_available']}")
    print(f"Default model ready: {health['default_model_ready']}")
    print(f"Generation test: {health['generation_test']}")
    
    return health

if __name__ == "__main__":
    test_ollama_connection()
