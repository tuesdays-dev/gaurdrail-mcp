import json
import requests
import os
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod


class AIClient(ABC):
    """Abstract base class for AI API clients"""
    
    @abstractmethod
    def generate_response(self, prompt: str, context: str) -> Dict[str, Any]:
        """Generate a response from the AI model"""
        pass


class OpenAIClient(AIClient):
    """OpenAI API client"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key must be provided either as parameter or OPENAI_API_KEY environment variable")
        self.model = model
        self.base_url = "https://api.openai.com/v1/chat/completions"
    
    def generate_response(self, prompt: str, context: str) -> Dict[str, Any]:
        """Generate response using OpenAI API"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Construct the message with context
        full_prompt = f"Context: {context}\n\nPrompt: {prompt}\n\nPlease respond in JSON format."
        
        data = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": full_prompt}
            ],
            "response_format": {"type": "json_object"}
        }
        
        try:
            response = requests.post(self.base_url, headers=headers, json=data)
            response.raise_for_status()
            
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            
            # Parse the JSON response
            return {
                "success": True,
                "response": json.loads(content),
                "raw_response": content,
                "usage": result.get("usage", {})
            }
            
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": f"Request error: {str(e)}"}
        except json.JSONDecodeError as e:
            return {"success": False, "error": f"JSON decode error: {str(e)}"}
        except Exception as e:
            return {"success": False, "error": f"Unexpected error: {str(e)}"}


class OllamaClient(AIClient):
    """Ollama API client"""
    
    def __init__(self, base_url: Optional[str] = None, model: Optional[str] = None):
        self.base_url = (base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")).rstrip('/')
        self.model = model or os.getenv("OLLAMA_MODEL", "llama2")
        self.endpoint = f"{self.base_url}/api/generate"
    
    def generate_response(self, prompt: str, context: str) -> Dict[str, Any]:
        """Generate response using Ollama API"""
        # Construct the message with context
        full_prompt = f"Context: {context}\n\nPrompt: {prompt}\n\nPlease respond in JSON format."
        
        data = {
            "model": self.model,
            "prompt": full_prompt,
            "stream": False,
            "format": "json"
        }
        
        try:
            response = requests.post(self.endpoint, json=data)
            response.raise_for_status()
            
            result = response.json()
            content = result.get("response", "")
            
            # Parse the JSON response
            return {
                "success": True,
                "response": json.loads(content),
                "raw_response": content,
                "model": result.get("model"),
                "created_at": result.get("created_at"),
                "done": result.get("done")
            }
            
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": f"Request error: {str(e)}"}
        except json.JSONDecodeError as e:
            return {"success": False, "error": f"JSON decode error: {str(e)}"}
        except Exception as e:
            return {"success": False, "error": f"Unexpected error: {str(e)}"}


class AIApp:
    """Main application class to handle AI interactions"""
    
    def __init__(self):
        self.client: Optional[AIClient] = None
    
    def setup_openai(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        """Setup OpenAI client"""
        self.client = OpenAIClient(api_key, model)
        return self
    
    def setup_ollama(self, base_url: Optional[str] = None, model: Optional[str] = None):
        """Setup Ollama client"""
        self.client = OllamaClient(base_url, model)
        return self
    
    def query(self, prompt: str, context: str) -> Dict[str, Any]:
        """Send query to the configured AI client"""
        if not self.client:
            return {"success": False, "error": "No AI client configured"}
        
        return self.client.generate_response(prompt, context)