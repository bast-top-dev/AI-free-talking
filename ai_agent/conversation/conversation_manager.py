"""
Conversation management for the AI Agent application.
"""

import random
from datetime import datetime
from typing import List, Optional, Callable, Dict, Any
from ..config.settings import (
    PREDEFINED_QUESTIONS, 
    RESPONSE_TEMPLATES, 
    KEYWORD_MAPPINGS
)


class ConversationManager:
    """Manages conversation flow and response generation."""
    
    def __init__(self):
        """Initialize the conversation manager."""
        self.conversation_history: List[Dict[str, Any]] = []
        self.user_responses: List[str] = []
        self.current_question_index = 0
        self.is_active = False
        self.history_callback: Optional[Callable] = None
        self.status_callback: Optional[Callable] = None
    
    def set_history_callback(self, callback: Callable):
        """Set callback for conversation history updates."""
        self.history_callback = callback
    
    def set_status_callback(self, callback: Callable):
        """Set callback for status updates."""
        self.status_callback = callback
    
    def _update_status(self, message: str):
        """Update status via callback."""
        if self.status_callback:
            self.status_callback(message)
    
    def _add_to_history(self, speaker: str, message: str):
        """Add message to conversation history."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        entry = {
            'timestamp': timestamp,
            'speaker': speaker,
            'message': message
        }
        self.conversation_history.append(entry)
        
        if self.history_callback:
            self.history_callback(entry)
    
    def start_conversation(self):
        """Start a new conversation."""
        self.is_active = True
        self.current_question_index = 0
        self._update_status("会話開始中...")
        
        # Ask the first question
        if self.current_question_index < len(PREDEFINED_QUESTIONS):
            question = PREDEFINED_QUESTIONS[self.current_question_index]
            self._add_to_history("ボット", question)
            self.current_question_index += 1
            return question
        return None
    
    def stop_conversation(self):
        """Stop the current conversation."""
        self.is_active = False
        self._update_status("会話停止")
    
    def process_user_response(self, response: str) -> Optional[str]:
        """
        Process user response and generate bot reply.
        
        Args:
            response: User's spoken or typed response
            
        Returns:
            Bot's response message
        """
        if not self.is_active:
            return None
        
        # Add user response to history
        self.user_responses.append(response)
        self._add_to_history("ユーザー", response)
        
        # Generate bot response
        bot_response = self._generate_response(response)
        if bot_response:
            self._add_to_history("ボット", bot_response)
        
        return bot_response
    
    def _generate_response(self, user_response: str) -> str:
        """Generate appropriate response based on user input."""
        # Check if we have predefined questions to ask
        if self.current_question_index < len(PREDEFINED_QUESTIONS):
            response = PREDEFINED_QUESTIONS[self.current_question_index]
            self.current_question_index += 1
            return response
        
        # Generate contextual response based on keywords
        response_category = self._categorize_response(user_response)
        
        if response_category in RESPONSE_TEMPLATES:
            responses = RESPONSE_TEMPLATES[response_category]
            return random.choice(responses)
        
        # Default response
        return random.choice(RESPONSE_TEMPLATES["default"])
    
    def _categorize_response(self, response: str) -> str:
        """Categorize user response based on keywords."""
        response_lower = response.lower()
        
        for category, keywords in KEYWORD_MAPPINGS.items():
            if any(keyword in response for keyword in keywords):
                return category
        
        return "default"
    
    def send_manual_message(self, message: str) -> Optional[str]:
        """
        Send a manual text message from user.
        
        Args:
            message: Manual text message
            
        Returns:
            Bot's response
        """
        return self.process_user_response(message)
    
    def get_next_question(self) -> Optional[str]:
        """Get the next predefined question."""
        if self.current_question_index < len(PREDEFINED_QUESTIONS):
            question = PREDEFINED_QUESTIONS[self.current_question_index]
            self.current_question_index += 1
            return question
        return None
    
    def reset_conversation(self):
        """Reset conversation to initial state."""
        self.conversation_history.clear()
        self.user_responses.clear()
        self.current_question_index = 0
        self.is_active = False
        self._update_status("会話を初期化しました")
    
    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history.clear()
        self._update_status("ログをクリアしました")
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        """Get summary of current conversation."""
        return {
            'total_messages': len(self.conversation_history),
            'user_messages': len(self.user_responses),
            'bot_messages': len(self.conversation_history) - len(self.user_responses),
            'current_question_index': self.current_question_index,
            'is_active': self.is_active
        }
    
    def export_conversation(self, filename: str):
        """Export conversation to file."""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("AI エージェント - 会話ログ\n")
                f.write("=" * 50 + "\n\n")
                
                for entry in self.conversation_history:
                    f.write(f"[{entry['timestamp']}] {entry['speaker']}: {entry['message']}\n\n")
            
            self._update_status(f"会話を {filename} にエクスポートしました")
        except Exception as e:
            self._update_status(f"エクスポートエラー: {str(e)}")
    
    def is_conversation_active(self) -> bool:
        """Check if conversation is currently active."""
        return self.is_active
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Get full conversation history."""
        return self.conversation_history.copy()
