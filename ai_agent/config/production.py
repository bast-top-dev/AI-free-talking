"""
Production configuration settings for the AI Agent application.
"""

import os
from .settings import *

# Production-specific overrides
DEBUG_MODE = False
LOG_LEVEL = "INFO"

# File paths for production
LOG_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "logs", "ai_agent.log")
CONVERSATION_LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "logs", "conversations")

# Create logs directory if it doesn't exist
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
os.makedirs(CONVERSATION_LOG_DIR, exist_ok=True)

# Production speech settings
DEFAULT_VOLUME = float(os.getenv('DEFAULT_VOLUME', '0.8'))
DEFAULT_VOICE_RATE = int(os.getenv('DEFAULT_VOICE_RATE', '150'))
SPEECH_TIMEOUT = int(os.getenv('SPEECH_TIMEOUT', '5'))
PHRASE_TIME_LIMIT = int(os.getenv('PHRASE_TIME_LIMIT', '10'))

# Production conversation settings
MAX_CONVERSATION_HISTORY = int(os.getenv('MAX_CONVERSATION_HISTORY', '1000'))
AUTO_SAVE_INTERVAL = int(os.getenv('AUTO_SAVE_INTERVAL', '300'))  # 5 minutes

# Security settings
ENABLE_INPUT_VALIDATION = True
MAX_INPUT_LENGTH = 500
ENABLE_CONVERSATION_LOGGING = True

# Performance settings
ENABLE_AUDIO_BUFFERING = True
AUDIO_BUFFER_SIZE = 1024
MAX_CONCURRENT_THREADS = 4
