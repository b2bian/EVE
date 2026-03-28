"""
Gemini API Handler - Uses Google's advanced Gemini model for better AI responses
With streaming support and fallback to Ollama if needed
"""

import os
import threading

# Try to import Gemini API components
try:
    from google.generativeai.client import configure
    from google.generativeai.generative_models import GenerativeModel
    from google.generativeai.types import GenerationConfig, HarmCategory, HarmBlockThreshold
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("Warning: google-generativeai not installed. Install with: pip install google-generativeai")

class GeminiHandler:
    """Handles communication with Google Gemini API."""
    
    def __init__(self, config=None):
        self.config = config or {}
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.is_connected = False
        self.model = "gemini-1.5-flash"  # Fast, high-quality responses
        
        if not GEMINI_AVAILABLE:
            print("Gemini API not available - install with: pip install google-generativeai")
            return
        
        if self.api_key:
            try:
                configure(api_key=self.api_key)  # type: ignore
                self.is_connected = True
                print(f"✓ Gemini API connected - using {self.model}")
            except Exception as e:
                print(f"Error connecting to Gemini: {e}")
                self.is_connected = False
        else:
            print("Note: GEMINI_API_KEY environment variable not set")
    
    def check_connection(self):
        """Verify Gemini API is accessible."""
        return self.is_connected
    
    def generate(self, prompt, stream=False, callback=None):
        """Generate response from Gemini with optional streaming."""
        if not GEMINI_AVAILABLE:
            return "Error: Gemini library not installed"
        
        if not self.is_connected:
            return "Error: Gemini API not configured"
        
        try:
            # Configure generation settings for quality
            generation_config = GenerationConfig(  # type: ignore
                temperature=0.7,  # Balanced creativity
                top_p=0.95,
                top_k=40,
                max_output_tokens=2048,
            )
            
            # Safety settings using proper enum values
            safety_settings = {
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,  # type: ignore
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,  # type: ignore
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,  # type: ignore
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,  # type: ignore
            }
            
            model = GenerativeModel(  # type: ignore
                self.model,
                generation_config=generation_config,
                safety_settings=safety_settings
            )
            
            if stream:
                # Streaming response
                full_response = ""
                response = model.generate_content(prompt, stream=True)
                
                for chunk in response:
                    if chunk.text:
                        full_response += chunk.text
                        if callback:
                            callback(chunk.text)
                
                return full_response
            else:
                # Standard response
                response = model.generate_content(prompt)
                return response.text if response.text else "No response generated"
                
        except Exception as e:
            error_msg = f"Gemini API error: {str(e)}"
            print(error_msg)
            # Disable Gemini connection on repeated errors such as API disabled or auth failure
            self.is_connected = False
            return error_msg
    
    def generate_async(self, prompt, callback=None):
        """Generate response asynchronously."""
        if not GEMINI_AVAILABLE:
            return False
        
        thread = threading.Thread(
            target=lambda: self.generate(prompt, stream=True, callback=callback)
        )
        thread.daemon = True
        thread.start()
        return True

