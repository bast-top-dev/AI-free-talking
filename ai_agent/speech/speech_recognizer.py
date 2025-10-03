"""
Speech Recognition engine for the AI Agent application.
"""

import speech_recognition as sr
import threading
from typing import Optional, Callable
import queue


class SpeechRecognizer:
    """Speech recognition engine with Japanese language support."""
    
    def __init__(self, language: str = 'ja-JP', timeout: int = 5, phrase_time_limit: int = 10):
        """
        Initialize the speech recognizer.
        
        Args:
            language: Language code for speech recognition
            timeout: Timeout in seconds for listening
            phrase_time_limit: Maximum time for a phrase
        """
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.language = language
        self.timeout = timeout
        self.phrase_time_limit = phrase_time_limit
        self.status_callback: Optional[Callable] = None
        self._audio_queue = queue.Queue()
        self._is_listening = False
        
        # Adjust for ambient noise
        self._calibrate_microphone()
    
    def _calibrate_microphone(self):
        """Calibrate microphone for ambient noise."""
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
        except Exception as e:
            print(f"Warning: Failed to calibrate microphone: {str(e)}")
    
    def set_status_callback(self, callback: Callable):
        """Set callback function for status updates."""
        self.status_callback = callback
    
    def _update_status(self, message: str):
        """Update status via callback."""
        if self.status_callback:
            self.status_callback(message)
    
    def listen_for_speech(self) -> Optional[str]:
        """
        Listen for speech input and return recognized text.
        
        Returns:
            Recognized text or None if no speech detected
        """
        try:
            self._update_status("音声を聞いています...")
            self._is_listening = True
            
            with self.microphone as source:
                audio = self.recognizer.listen(
                    source, 
                    timeout=self.timeout, 
                    phrase_time_limit=self.phrase_time_limit
                )
            
            self._update_status("音声認識中...")
            
            # Recognize speech using Google Speech Recognition
            text = self.recognizer.recognize_google(audio, language=self.language)
            self._update_status("音声認識完了")
            self._is_listening = False
            return text
            
        except sr.WaitTimeoutError:
            self._update_status("音声入力タイムアウト")
            self._is_listening = False
            return None
        except sr.UnknownValueError:
            self._update_status("音声が認識できませんでした")
            self._is_listening = False
            return None
        except sr.RequestError as e:
            self._update_status(f"音声認識サービスエラー: {str(e)}")
            self._is_listening = False
            return None
        except Exception as e:
            self._update_status(f"音声認識エラー: {str(e)}")
            self._is_listening = False
            return None
    
    def listen_continuous(self, callback: Callable[[str], None], stop_event: threading.Event):
        """
        Continuously listen for speech in a separate thread.
        
        Args:
            callback: Function to call with recognized text
            stop_event: Event to signal when to stop listening
        """
        def listen_worker():
            while not stop_event.is_set():
                text = self.listen_for_speech()
                if text:
                    callback(text)
                if stop_event.wait(0.1):  # Small delay to prevent busy waiting
                    break
        
        thread = threading.Thread(target=listen_worker)
        thread.daemon = True
        thread.start()
        return thread
    
    def is_listening(self) -> bool:
        """Check if currently listening for speech."""
        return self._is_listening
    
    def stop_listening(self):
        """Stop current listening operation."""
        self._is_listening = False
    
    def get_microphone_list(self):
        """Get list of available microphones."""
        return sr.Microphone.list_microphone_names()
    
    def set_microphone(self, device_index: int):
        """Set specific microphone device."""
        try:
            self.microphone = sr.Microphone(device_index=device_index)
            self._calibrate_microphone()
        except Exception as e:
            raise RuntimeError(f"Failed to set microphone: {str(e)}")
    
    def test_microphone(self) -> bool:
        """Test if microphone is working properly."""
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=2)
            return True
        except:
            return False
