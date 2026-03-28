import subprocess
import requests
import time
from typing import Optional

class OllamaManager:
    def __init__(self, host: str = "localhost", port: int = 11434):
        self.host = host
        self.port = port
        self.base_url = f"http://{host}:{port}"
        self.process: Optional[subprocess.Popen] = None
    
    def is_running(self) -> bool:
        """Check if Ollama server is responding"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=1)
            return response.status_code == 200
        except:
            return False
    
    def ensure_running(self):
        """Start Ollama if not already running"""
        if self.is_running():
            return True
        
        print("Starting Ollama...")
        try:
            self.process = subprocess.Popen(
                ["ollama", "serve"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            for i in range(30):
                time.sleep(0.5)
                if self.is_running():
                    print("✓ Ollama started")
                    return True
            
            print("✗ Ollama failed to start")
            return False
        except Exception as e:
            print(f"✗ Error starting Ollama: {e}")
            return False
    
    def get_available_models(self) -> list:
        """List available Ollama models"""
        if not self.is_running():
            return []
        
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            models = response.json().get("models", [])
            return [m["name"] for m in models]
        except:
            return []
    
    def generate(self, prompt: str, model: str = "mistral") -> str:
        """Generate response from Ollama"""
        if not self.is_running():
            return "Error: Ollama not running"
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.7
                },
                timeout=60
            )
            
            if response.status_code == 200:
                return response.json().get("response", "")
            else:
                return f"Error: {response.status_code}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def get_status(self) -> dict:
        """Get Ollama health status"""
        return {
            "running": self.is_running(),
            "models": self.get_available_models(),
            "host": self.host,
            "port": self.port,
            "url": self.base_url
        }
