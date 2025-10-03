"""
Main application entry point for the AI Agent.
"""

import threading
import time
import os
import sys
import logging
from ai_agent.ui.main_window import MainWindow
from ai_agent.speech.tts_engine import TTSEngine
from ai_agent.speech.speech_recognizer import SpeechRecognizer
from ai_agent.conversation.conversation_manager import ConversationManager
from ai_agent.config.settings import DEFAULT_VOLUME, DEFAULT_VOICE_RATE

# Production configuration
PRODUCTION_MODE = os.getenv('PRODUCTION_MODE', 'False').lower() == 'true'


class AIAgentApplication:
    """Main application class that coordinates all components."""
    
    def __init__(self):
        """Initialize the AI Agent application."""
        # Setup logging for production
        self._setup_logging()
        
        # Initialize components
        self.ui = MainWindow()
        self.tts_engine = TTSEngine(volume=DEFAULT_VOLUME, rate=DEFAULT_VOICE_RATE)
        self.speech_recognizer = SpeechRecognizer()
        self.conversation_manager = ConversationManager()
        
        # Threading
        self.conversation_thread = None
        self.stop_event = threading.Event()
        
        # Setup component connections
        self._setup_callbacks()
    
    def _setup_logging(self):
        """Setup logging configuration."""
        if PRODUCTION_MODE:
            # Production logging
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                handlers=[
                    logging.FileHandler('ai_agent.log'),
                    logging.StreamHandler()
                ]
            )
        else:
            # Development logging
            logging.basicConfig(
                level=logging.DEBUG,
                format='%(levelname)s - %(message)s'
            )
    
    def _setup_callbacks(self):
        """Setup callbacks between components."""
        # UI callbacks
        self.ui.set_start_callback(self.start_conversation)
        self.ui.set_stop_callback(self.stop_conversation)
        self.ui.set_send_text_callback(self.send_text_message)
        self.ui.set_clear_log_callback(self.clear_log)
        self.ui.set_init_conversation_callback(self.initialize_conversation)
        self.ui.set_volume_change_callback(self.update_volume)
        
        # Speech engine callbacks
        self.tts_engine.set_voice_callback(self.ui.update_voice_visualization)
        
        # Speech recognizer callbacks
        self.speech_recognizer.set_status_callback(self.ui.update_status)
        
        # Conversation manager callbacks
        self.conversation_manager.set_history_callback(self.ui.add_to_history)
        self.conversation_manager.set_status_callback(self.ui.update_status)
    
    def start_conversation(self):
        """Start the conversation."""
        try:
            # Start conversation in manager
            initial_message = self.conversation_manager.start_conversation()
            
            # Update UI state
            self.ui.set_conversation_state(True)
            
            # Speak initial message
            if initial_message:
                self.tts_engine.speak(initial_message)
            
            # Start conversation loop in separate thread
            self.stop_event.clear()
            self.conversation_thread = threading.Thread(target=self._conversation_loop)
            self.conversation_thread.daemon = True
            self.conversation_thread.start()
            
        except Exception as e:
            self.ui.show_error("エラー", f"会話開始エラー: {str(e)}")
            self.ui.update_status("会話開始エラー")
    
    def stop_conversation(self):
        """Stop the conversation."""
        try:
            # Stop conversation manager
            self.conversation_manager.stop_conversation()
            
            # Signal stop event
            self.stop_event.set()
            
            # Stop TTS engine
            self.tts_engine.stop()
            
            # Update UI state
            self.ui.set_conversation_state(False)
            
        except Exception as e:
            self.ui.show_error("エラー", f"会話停止エラー: {str(e)}")
    
    def _conversation_loop(self):
        """Main conversation loop running in separate thread."""
        try:
            while not self.stop_event.is_set() and self.conversation_manager.is_conversation_active():
                # Listen for user speech
                user_response = self.speech_recognizer.listen_for_speech()
                
                if user_response and not self.stop_event.is_set():
                    # Process user response and get bot reply
                    bot_response = self.conversation_manager.process_user_response(user_response)
                    
                    # Speak bot response
                    if bot_response:
                        self.tts_engine.speak(bot_response)
                
                # Small delay to prevent busy waiting
                if self.stop_event.wait(0.5):
                    break
                    
        except Exception as e:
            self.ui.update_status(f"会話ループエラー: {str(e)}")
        finally:
            # Ensure UI is updated even if thread ends unexpectedly
            self.ui.set_conversation_state(False)
    
    def send_text_message(self, text: str):
        """Send manual text message."""
        try:
            # Process message through conversation manager
            bot_response = self.conversation_manager.send_manual_message(text)
            
            # Speak bot response if conversation is active
            if bot_response and self.conversation_manager.is_conversation_active():
                self.tts_engine.speak(bot_response)
                
        except Exception as e:
            self.ui.show_error("エラー", f"メッセージ送信エラー: {str(e)}")
    
    def clear_log(self):
        """Clear conversation log."""
        try:
            self.conversation_manager.clear_history()
            self.ui.clear_history()
        except Exception as e:
            self.ui.show_error("エラー", f"ログクリアエラー: {str(e)}")
    
    def initialize_conversation(self):
        """Initialize conversation to start."""
        try:
            # Stop current conversation if active
            if self.conversation_manager.is_conversation_active():
                self.stop_conversation()
            
            # Reset conversation manager
            self.conversation_manager.reset_conversation()
            
            # Clear UI history
            self.ui.clear_history()
            
        except Exception as e:
            self.ui.show_error("エラー", f"初期化エラー: {str(e)}")
    
    def update_volume(self, volume: float):
        """Update TTS engine volume."""
        try:
            self.tts_engine.set_volume(volume)
        except Exception as e:
            self.ui.update_status(f"音量設定エラー: {str(e)}")
    
    def run(self):
        """Run the application."""
        try:
            # Initialize status
            self.ui.update_status("アプリケーション準備完了")
            
            # Start the UI main loop
            self.ui.run()
            
        except Exception as e:
            self.ui.show_error("致命的エラー", f"アプリケーションエラー: {str(e)}")
        finally:
            self._cleanup()
    
    def _cleanup(self):
        """Clean up resources."""
        try:
            # Stop conversation
            self.stop_conversation()
            
            # Cleanup components
            self.tts_engine.cleanup()
            
        except Exception as e:
            print(f"Cleanup error: {str(e)}")


def handle_exception(exc_type, exc_value, exc_traceback):
    """Global exception handler."""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    
    logging.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

def main():
    """Main entry point."""
    # Setup global exception handler
    sys.excepthook = handle_exception
    
    try:
        logging.info("Starting AI Agent application...")
        app = AIAgentApplication()
        app.run()
    except Exception as e:
        logging.critical(f"Failed to start application: {str(e)}")
        print(f"Failed to start application: {str(e)}")
    finally:
        logging.info("AI Agent application stopped.")


if __name__ == "__main__":
    main()
