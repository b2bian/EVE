import threading
import json

try:
    from faster_whisper import WhisperModel
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False
    WhisperModel = None

try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    pyttsx3 = None

class VoiceHandler:
    """Handles voice input/output using Faster-Whisper and pyttsx3."""
    
    def __init__(self, config, on_transcript_callback=None):
        self.config = config
        self.is_listening = False
        self.on_transcript = on_transcript_callback
        self.model = None
        self.tts_engine = None
        self.last_transcript = ""
        self.load_model()
        self.load_tts_engine()
    
    def load_model(self):
        """Load Whisper model."""
        if not WHISPER_AVAILABLE:
            print("Note: Faster-Whisper not available. Voice features disabled.")
            print("To enable: pip install faster-whisper")
            return False
        
        try:
            model_size = self.config.get("voice", {}).get("model", "base")
            self.model = WhisperModel(
                model_size,
                device="cpu",
                compute_type="int8"
            )
            return True
        except Exception as e:
            print(f"Error loading voice model: {e}")
            return False
    
    def load_tts_engine(self):
        """Load text-to-speech engine."""
        if not TTS_AVAILABLE:
            print("Note: pyttsx3 not available. Text-to-speech disabled.")
            return False
        
        try:
            self.tts_engine = pyttsx3.init()
            # Configure voice - default to first female voice if available
            self._set_default_female_voice()
            # Configure voice properties
            self.tts_engine.setProperty('rate', 150)  # Speed
            self.tts_engine.setProperty('volume', 0.9)  # Volume
            return True
        except Exception as e:
            print(f"Error loading TTS engine: {e}")
            return False
    
    def get_available_voices(self):
        """Get list of available voices (female voices preferred)."""
        if not self.tts_engine:
            return []
        
        try:
            voices = self.tts_engine.getProperty('voices')
            voice_list = []
            
            # Comprehensive list of known female voice names (macOS and common TTS systems)
            female_voice_names = {
                'alice', 'alva', 'amelie', 'anna', 'balloons', 'bergamot', 'breeze',
                'bubu', 'carmit', 'celia', 'damayanti', 'diana', 'eden', 'ellen',
                'fiona', 'flora', 'hattie', 'hermes', 'iris', 'ioana', 'joana',
                'julia', 'kanya', 'karen', 'kyoko', 'laura', 'lekha', 'lena',
                'luciana', 'mariska', 'mei-jia', 'melina', 'milena', 'moira',
                'monica', 'nora', 'paulina', 'reina', 'samantha', 'sara', 'satu',
                'sirina', 'tessa', 'veena', 'victoria', 'yuki', 'yuna', 'zosia',
                'zuzana', 'susan', 'victoria', 'rose', 'emma', 'lily', 'rachel',
                'claire', 'catherine', 'margaret', 'judith', 'patricia', 'donna'
            }
            
            for voice in voices:
                voice_name = voice.name
                voice_id = voice.id
                # Check if voice name is in female voice list
                is_female = voice_name.lower() in female_voice_names
                voice_list.append({
                    'name': voice_name,
                    'id': voice_id,
                    'is_female': is_female
                })
            return voice_list
        except Exception as e:
            print(f"Error getting voices: {e}")
            return []
    
    def _set_default_female_voice(self):
        """Set default voice to a female voice if available."""
        try:
            voices = self.tts_engine.getProperty('voices')
            # Comprehensive list of known female voice names (preferred order)
            preferred_female_voices = ['victoria', 'samantha', 'moira', 'karen', 'fiona', 
                                       'alice', 'amelie', 'anna', 'anna', 'laura', 'ellen']
            
            # First try to find a preferred female voice
            for preferred in preferred_female_voices:
                for voice in voices:
                    if preferred.lower() in voice.name.lower():
                        self.tts_engine.setProperty('voice', voice.id)
                        return
            
            # If no preferred voice found, look for any female voice
            female_voice_names = {
                'alice', 'alva', 'amelie', 'anna', 'balloons', 'bergamot', 'breeze',
                'bubu', 'carmit', 'celia', 'damayanti', 'diana', 'eden', 'ellen',
                'fiona', 'flora', 'hattie', 'hermes', 'iris', 'ioana', 'joana',
                'julia', 'kanya', 'karen', 'kyoko', 'laura', 'lekha', 'lena',
                'luciana', 'mariska', 'mei-jia', 'melina', 'milena', 'moira',
                'monica', 'nora', 'paulina', 'reina', 'samantha', 'sara', 'satu',
                'sirina', 'tessa', 'veena', 'victoria', 'yuki', 'yuna', 'zosia',
                'zuzana', 'susan', 'victoria', 'rose', 'emma', 'lily', 'rachel',
                'claire', 'catherine', 'margaret', 'judith', 'patricia', 'donna'
            }
            
            for voice in voices:
                if voice.name.lower() in female_voice_names:
                    self.tts_engine.setProperty('voice', voice.id)
                    return
            
            # If no female voice found, use first available voice
            if voices:
                self.tts_engine.setProperty('voice', voices[0].id)
        except Exception as e:
            print(f"Error setting female voice: {e}")
    
    def set_voice(self, voice_id):
        """Set specific voice by ID."""
        if not self.tts_engine:
            return False
        
        try:
            self.tts_engine.setProperty('voice', voice_id)
            return True
        except Exception as e:
            print(f"Error setting voice: {e}")
            return False
    
    def start_listening(self):
        """Start listening for voice input."""
        if self.is_listening:
            return
        
        self.is_listening = True
        # Start recording in a separate thread
        thread = threading.Thread(target=self._record_and_transcribe)
        thread.daemon = True
        thread.start()
    
    def stop_listening(self):
        """Stop listening."""
        self.is_listening = False
    
    def _record_and_transcribe(self):
        """Record audio and transcribe it."""
        try:
            import pyaudio
            import wave
            import tempfile
            
            # Audio recording parameters
            CHUNK = 1024
            FORMAT = pyaudio.paFloat32
            CHANNELS = 1
            RATE = 16000
            
            pa = pyaudio.PyAudio()
            
            # Create temporary file for audio
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                temp_file = tmp.name
            
            # Start recording
            stream = pa.open(
                format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK
            )
            
            frames = []
            while self.is_listening:
                try:
                    data = stream.read(CHUNK, exception_on_overflow=False)
                    frames.append(data)
                except Exception as e:
                    print(f"Recording error: {e}")
                    break
            
            # Save audio file
            stream.stop_stream()
            stream.close()
            pa.terminate()
            
            with wave.open(temp_file, 'wb') as wf:
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(pa.get_sample_size(FORMAT))
                wf.setframerate(RATE)
                wf.writeframes(b''.join(frames))
            
            # Transcribe
            if self.model and len(frames) > 0:
                segments, info = self.model.transcribe(temp_file)
                transcript = " ".join([segment.text for segment in segments])
                self.last_transcript = transcript.strip()

                if self.on_transcript:
                    try:
                        self.on_transcript(self.last_transcript)
                    except Exception as callback_e:
                        print(f"Voice callback error: {callback_e}")

                # Clean up
                import os
                os.unlink(temp_file)
        
        except Exception as e:
            print(f"Voice transcription error: {e}")
    
    def is_model_loaded(self):
        """Check if model is loaded."""
        return self.model is not None

    def get_last_transcript(self):
        """Return the last transcript captured by voice recorder."""
        return self.last_transcript
    
    def transcribe_file(self, file_path):
        """Transcribe audio file to text."""
        if not self.model:
            return None
        
        try:
            segments, info = self.model.transcribe(file_path)
            transcript = " ".join([segment.text for segment in segments])
            return transcript.strip() if transcript else None
        except Exception as e:
            print(f"Transcription error: {e}")
            return None
    
    def speak(self, text):
        """Speak text using TTS engine."""
        if not self.tts_engine:
            print("TTS engine not available")
            return False
        
        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
            return True
        except Exception as e:
            print(f"TTS error: {e}")
            return False
    
    def speak_async(self, text):
        """Speak text asynchronously (non-blocking)."""
        if not self.tts_engine:
            return False
        
        thread = threading.Thread(target=lambda: self.speak(text))
        thread.daemon = True
        thread.start()
        return True
    
    def set_voice_rate(self, rate):
        """Set speech rate (50-300, default 150)."""
        if self.tts_engine:
            self.tts_engine.setProperty('rate', rate)
    
    def set_voice_volume(self, volume):
        """Set volume (0.0-1.0, default 0.9)."""
        if self.tts_engine:
            self.tts_engine.setProperty('volume', volume)
