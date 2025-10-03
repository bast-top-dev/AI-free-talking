"""
Text-to-Speech engine for the AI Agent application.
"""

import pyttsx3
import threading
import random
from typing import Optional, Callable


class TTSEngine:
    """Text-to-Speech engine with Japanese voice support."""
    
    def __init__(self, volume: float = 0.8, rate: int = 150):
        """
        Initialize the TTS engine.
        
        Args:
            volume: Volume level (0.0 to 1.0)
            rate: Speech rate (words per minute)
        """
        self.engine = None
        self.volume = volume
        self.rate = rate
        self.voice_callback: Optional[Callable] = None
        self._initialize_engine()
    
    def _initialize_engine(self):
        """Initialize the pyttsx3 engine with Japanese voice settings."""
        try:
            self.engine = pyttsx3.init()
            
            # Set Japanese female voice
            voices = self.engine.getProperty('voices')
            japanese_voice = None
            
            for voice in voices:
                if 'japanese' in voice.name.lower() or 'ja' in voice.id.lower():
                    japanese_voice = voice
                    break
            
            if japanese_voice:
                self.engine.setProperty('voice', japanese_voice.id)
            
            # Set voice properties
            self.engine.setProperty('rate', self.rate)
            self.engine.setProperty('volume', self.volume)
            
        except ImportError as e:
            if 'pywintypes' in str(e):
                raise RuntimeError(
                    "PyWinTypes module not found. This is common with Python 3.13+ on Windows.\n"
                    "Please run: fix_pywintypes.bat or fix_pywintypes.py\n"
                    "Or use Python 3.11 for better compatibility."
                )
            else:
                raise RuntimeError(f"Failed to import required modules: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Failed to initialize TTS engine: {str(e)}")
    
    def set_volume(self, volume: float):
        """Set the volume level."""
        self.volume = max(0.0, min(1.0, volume))
        if self.engine:
            self.engine.setProperty('volume', self.volume)
    
    def set_rate(self, rate: int):
        """Set the speech rate."""
        self.rate = rate
        if self.engine:
            self.engine.setProperty('rate', self.rate)
    
    def set_voice_callback(self, callback: Callable):
        """Set callback function for voice visualization."""
        self.voice_callback = callback
    
    def speak(self, text: str, blocking: bool = True):
        """
        Speak the given text.
        
        Args:
            text: Text to speak
            blocking: Whether to block until speech is complete
        """
        if not self.engine:
            raise RuntimeError("TTS engine not initialized")
        
        if self.voice_callback:
            self._animate_voice()
        
        try:
            self.engine.say(text)
            if blocking:
                self.engine.runAndWait()
            else:
                # Run in separate thread for non-blocking speech
                thread = threading.Thread(target=self.engine.runAndWait)
                thread.daemon = True
                thread.start()
                return thread
        except Exception as e:
            raise RuntimeError(f"Failed to speak text: {str(e)}")
    
    def _animate_voice(self):
        """Animate voice visualization if callback is set."""
        if self.voice_callback:
            # Generate random pitch pattern for visualization
            pitch_data = []
            for i in range(10):
                height = random.randint(20, 120)
                color = f"#{random.randint(100, 255):02x}{random.randint(100, 255):02x}{random.randint(100, 255):02x}"
                pitch_data.append((i * 10, height, color))
            
            self.voice_callback(pitch_data)
    
    def stop(self):
        """Stop current speech."""
        if self.engine:
            self.engine.stop()
    
    def get_available_voices(self):
        """Get list of available voices."""
        if not self.engine:
            return []
        
        voices = self.engine.getProperty('voices')
        return [{'id': voice.id, 'name': voice.name} for voice in voices]
    
    def cleanup(self):
        """Clean up the TTS engine."""
        if self.engine:
            self.engine.stop()
            del self.engine
            self.engine = None
