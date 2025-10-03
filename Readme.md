# AI Agent - Japanese Sales Call Bot

A sophisticated AI-powered conversational agent built with Python, designed for Japanese sales calls. Features speech recognition, text-to-speech, and intelligent conversation management.

## 🚀 Quick Start

### Windows Users (Easiest)
```bash
# Double-click to run
start_ai_agent.bat
```

### Linux/macOS Users
```bash
# Make executable and run
chmod +x start_ai_agent.sh
./start_ai_agent.sh
```

### Manual Installation
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run application
python main.py
# or
python run.py
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.7 or higher
- Microphone and speakers
- Internet connection (for speech recognition)

### Windows Setup (Common Issues)

**PyAudio Installation Fix:**
The most common issue on Windows is PyAudio installation failure. Here's how to fix it:

```bash
# Method 1: Use pipwin (Recommended)
pip install pipwin
pipwin install pyaudio
pip install pyttsx3 speech_recognition

# Method 2: Use the fix script
fix_pyaudio.bat

# Method 3: Manual compilation (if above fails)
# Install Visual Studio Build Tools first
pip install pyaudio
```

**Alternative Windows Methods:**
```bash
# Using conda (if you have Anaconda/Miniconda)
conda create -n ai-agent python=3.9
conda activate ai-agent
conda install pyaudio
pip install pyttsx3 speech_recognition
```

### Linux Setup
```bash
# Ubuntu/Debian
sudo apt-get install python3-pyaudio portaudio19-dev
pip install -r requirements.txt

# CentOS/RHEL
sudo yum install portaudio-devel
pip install -r requirements.txt
```

### macOS Setup
```bash
# Install PortAudio first
brew install portaudio

# Install Python dependencies
pip install -r requirements.txt
```

## 📁 Project Structure

```
AI-free-talking/
├── ai_agent/                    # Main application package
│   ├── config/                  # Configuration management
│   │   ├── settings.py         # Application settings
│   │   └── production.py       # Production configuration
│   ├── ui/                     # User interface components
│   │   └── main_window.py      # Main application window
│   ├── speech/                 # Audio processing
│   │   ├── tts_engine.py       # Text-to-speech engine
│   │   └── speech_recognizer.py # Speech recognition
│   └── conversation/           # Conversation management
│       └── conversation_manager.py
├── main.py                     # Application entry point
├── run.py                      # Smart launcher with dependency checking
├── start_ai_agent.bat         # Windows launcher
├── start_ai_agent.sh          # Linux/macOS launcher
├── fix_pyaudio.bat            # Windows PyAudio fix script
├── requirements.txt            # Dependencies
└── README.md                  # This file
```

## 🎯 Features

### Core Functionality
- **Japanese Voice Output**: Female voice speaks in Japanese
- **Speech Recognition**: Understands Japanese speech input
- **Smart Conversation Flow**: Context-aware responses based on keywords
- **Real-time Display**: Live conversation history with timestamps
- **Manual Input**: Type messages if speech recognition fails
- **Volume Control**: Adjustable audio levels
- **Voice Visualization**: Real-time pitch/height visualization during speech

### UI Controls
- **開始 (Start)**: Begin conversation
- **停止 (Stop)**: End conversation
- **テキスト送信 (Send Text)**: Send manual text messages
- **ログクリア (Clear Log)**: Clear conversation history
- **会話初期化 (Initialize)**: Reset conversation to beginning
- **Volume Slider**: Adjust TTS volume (0-100%)

### Conversation Script
The bot follows a predefined rice sales script:
1. Introduces as "高木 from X商事"
2. Explains rice business for bento shops
3. Presents "近江ブレンド米・小粒タイプ" product
4. Mentions pricing (588円 per kg, tax excluded, shipping included)
5. Highlights small grain benefits for bento boxes
6. Offers free samples and requests store information

### Intelligent Responses
The bot generates contextual responses based on user input:
- **Interest keywords**: "興味", "関心", "詳しく", "サンプル" → Offers samples
- **Busy keywords**: "忙しい", "時間", "用事" → Acknowledges and speeds up
- **Price keywords**: "値段", "価格", "いくら" → Explains pricing
- **Quality keywords**: "米", "ご飯", "品質" → Describes product benefits

## 🏭 Production Deployment

### Standalone Executable (Windows)
```bash
# Install PyInstaller
pip install pyinstaller

# Create executable
pyinstaller --onefile --windowed --name "AI_Agent" main.py

# Executable will be in dist/ folder
```

### Docker Deployment
```dockerfile
# Create Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    python3-pyaudio \
    espeak \
    libespeak1 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Run application
CMD ["python", "main.py"]
```

```bash
# Build and run
docker build -t ai-agent .
docker run -it --device /dev/snd ai-agent
```

### System Service (Linux)
```ini
# Create /etc/systemd/system/ai-agent.service
[Unit]
Description=AI Agent Application
After=network.target

[Service]
Type=simple
User=aiagent
WorkingDirectory=/opt/ai-agent
ExecStart=/usr/bin/python3 /opt/ai-agent/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Install and start service
sudo systemctl enable ai-agent
sudo systemctl start ai-agent
```

### Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv ai_agent_env

# Activate (Windows)
ai_agent_env\Scripts\activate

# Activate (Linux/macOS)
source ai_agent_env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```

## 🔧 Configuration

### Environment Variables
```bash
# Production mode
export PRODUCTION_MODE=True

# Audio settings
export DEFAULT_VOLUME=0.8
export DEFAULT_VOICE_RATE=150
export SPEECH_TIMEOUT=5

# Conversation settings
export MAX_CONVERSATION_HISTORY=1000
export AUTO_SAVE_INTERVAL=300
```

### Configuration Files
- **`ai_agent/config/settings.py`**: Main application settings
- **`ai_agent/config/production.py`**: Production-specific overrides

### Customization
- **Questions**: Modify `PREDEFINED_QUESTIONS` in `settings.py`
- **Responses**: Update `RESPONSE_TEMPLATES` and `KEYWORD_MAPPINGS`
- **Voice Settings**: Adjust rate, volume, and language in TTS engine
- **UI**: Customize colors, fonts, and layout in `main_window.py`

## 🚨 Troubleshooting

### Common Issues

**PyAudio Installation (Windows)**
```bash
# Solution 1: Use pipwin
pip install pipwin
pipwin install pyaudio

# Solution 2: Install Visual Studio Build Tools
# Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/

# Solution 3: Use conda
conda install pyaudio
```

**Speech Recognition Not Working**
- Check internet connection (uses Google Speech API)
- Verify microphone permissions
- Test with different audio devices
- Try typing instead of speaking

**Audio Output Issues**
- Check speaker connections
- Verify audio drivers
- Test with different audio devices
- Adjust volume settings

**Application Crashes**
- Check console output for error messages
- Verify all dependencies are installed
- Test with minimal configuration
- Check system resources

### Debug Mode
```bash
# Enable debug logging
export DEBUG_MODE=True
python main.py
```

### Health Check
```python
# Test all components
python -c "
import pyttsx3, speech_recognition, tkinter
print('✓ All dependencies working')
"
```

## 🏗️ Architecture

### Modular Design
- **Separation of Concerns**: Each module has a single responsibility
- **Maintainability**: Easy to locate and modify specific functionality
- **Testability**: Components can be tested independently
- **Extensibility**: New features can be added without breaking existing code

### Key Components
- **MainWindow**: UI display and user interaction management
- **TTSEngine**: Text-to-speech synthesis with voice control
- **SpeechRecognizer**: Speech recognition and microphone management
- **ConversationManager**: Conversation flow and response generation
- **Settings**: Configuration management and constants

### Threading Model
- **Main Thread**: UI updates and user interactions
- **Conversation Thread**: Speech recognition and processing
- **TTS Thread**: Non-blocking speech synthesis

### Data Flow
```
User Input → UI → Main App → Conversation Manager → Response Generator
                ↓
            Speech Engine → Audio Output
                ↓
            UI Update → Display
```

## 📊 Performance & Scaling

### Optimization
- **Audio Buffering**: Reduces latency in speech processing
- **Memory Management**: Periodic cleanup of conversation history
- **Threading**: Non-blocking operations for better responsiveness

### Scaling Considerations
- **Multiple Users**: Implement user sessions and authentication
- **High Volume**: Use message queues and load balancing
- **Cloud Deployment**: Container orchestration with Kubernetes

## 🔒 Security & Privacy

### Data Handling
- **No Storage**: Conversation data is not permanently stored
- **Input Validation**: All user inputs are validated and sanitized
- **Error Handling**: Graceful degradation when components fail

### Production Security
- **Minimal Privileges**: Run with limited system access
- **Input Sanitization**: Prevent injection attacks
- **Rate Limiting**: Prevent abuse of speech recognition API

## 📈 Future Enhancements

### Planned Features
- **Multi-language Support**: Add support for other languages
- **Voice Cloning**: Custom voice training
- **Advanced NLP**: Better conversation understanding
- **Analytics Dashboard**: Conversation metrics and insights
- **API Integration**: REST API for external systems

### Extension Points
- **New Speech Engines**: Easy to swap TTS/STT providers
- **Custom UI Themes**: Pluggable UI components
- **Conversation Strategies**: Different conversation flows
- **Plugin System**: Third-party extensions

## 🤝 Contributing

### Development Setup
```bash
# Clone repository
git clone <repository-url>
cd AI-free-talking

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/
```

### Code Style
- Follow PEP 8 guidelines
- Use type hints where possible
- Add docstrings to all functions
- Write unit tests for new features

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

### Getting Help
1. Check this README for common solutions
2. Look at console output for error messages
3. Verify all dependencies are installed correctly
4. Test with minimal configuration

### Reporting Issues
When reporting issues, please include:
- Operating system and version
- Python version
- Complete error message
- Steps to reproduce the issue

---

**Ready to start? Just run the appropriate launcher script for your system!** 🎉

For Windows: `start_ai_agent.bat`  
For Linux/macOS: `./start_ai_agent.sh`  
Manual: `python main.py`

