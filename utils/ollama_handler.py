import requests
import json
import threading

class OllamaHandler:
    """Handles communication with Ollama LLM."""
    
    def __init__(self, config):
        self.config = config.get("ollama", {})
        self.base_url = self.config.get("base_url", "http://localhost:11434")
        self.model = self.config.get("model", "neural-chat")
        self.is_connected = False
        self.check_connection()
    
    def check_connection(self):
        """Check if Ollama is running."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            self.is_connected = response.status_code == 200
            return self.is_connected
        except Exception as e:
            print(f"Ollama connection error: {e}")
            self.is_connected = False
            return False
    
    def get_available_models(self):
        """Get list of available models."""
        if not self.is_connected:
            return []
        
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return [model["name"] for model in data.get("models", [])]
            return []
        except Exception as e:
            print(f"Error fetching models: {e}")
            return []
    
    def generate(self, prompt, stream=False, callback=None):
        """Generate response from Ollama."""
        if not self.is_connected:
            return "Error: Ollama is not running. Please start Ollama first."
        
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": stream,
                "temperature": self.config.get("temperature", 0.7),
                "top_p": self.config.get("top_p", 0.9),
                "top_k": self.config.get("top_k", 40)
            }
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=180
            )
            
            if response.status_code == 200:
                if stream:
                    full_response = ""
                    for line in response.iter_lines():
                        if line:
                            try:
                                data = json.loads(line)
                                chunk = data.get("response", "")
                                full_response += chunk
                                if callback:
                                    callback(chunk)
                            except json.JSONDecodeError:
                                pass
                    return full_response
                else:
                    data = response.json()
                    return data.get("response", "")
            else:
                return f"Error: HTTP {response.status_code}"
        
        except Exception as e:
            return f"Error: {str(e)}"
    
    def generate_async(self, prompt, callback):
        """Generate response asynchronously."""
        thread = threading.Thread(
            target=lambda: self.generate(prompt, stream=True, callback=callback)
        )
        thread.daemon = True
        thread.start()
    
    def switch_model(self, model_name):
        """Switch to a different model."""
        if model_name in self.get_available_models():
            self.model = model_name
            return True
        return False
    
    def system_message(self, user_name="User"):
        """Get system message for context."""
        return f"""You are EVE, a quirky female AI assistant with a cyberpunk personality. 
You assist {user_name} with coding, ideas, and creative projects.
Keep responses concise, punchy, and technically accurate.
Use occasional hacker/cyberpunk slang naturally.
Be helpful, witty, and remember context from the conversation."""
