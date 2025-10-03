# 🚀 AI Agent - Quick Start Guide

## 📋 What You Need
- Python 3.7 or higher
- Microphone and speakers
- Internet connection (for speech recognition)

## ⚡ Super Quick Start

### Windows Users
1. **Double-click** `start_ai_agent.bat`
2. Wait for dependencies to install (first time only)
3. The AI Agent window will open automatically

### Linux/macOS Users
1. Open terminal in the project folder
2. Run: `chmod +x start_ai_agent.sh && ./start_ai_agent.sh`
3. Wait for dependencies to install (first time only)
4. The AI Agent window will open automatically

## 🎯 How to Use

1. **Click "開始" (Start)** to begin conversation
2. **Speak naturally** - the bot will ask questions in Japanese
3. **Respond verbally** or type in the text box
4. **Click "停止" (Stop)** when done
5. **Use "ログクリア" (Clear Log)** to clear conversation history
6. **Adjust volume** with the slider on the right

## 🔧 Manual Installation (if needed)

```bash
# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```

## 🚨 Troubleshooting

### PyAudio Installation Error (Windows)
This is the most common issue on Windows. Use pipwin to fix it:

```bash
pip install pipwin
pipwin install pyaudio
pip install pyttsx3 speech_recognition
```

**See [WINDOWS_SETUP.md](WINDOWS_SETUP.md) for detailed Windows setup guide.**

### "No module named 'pyttsx3'" Error
```bash
pip install pyttsx3 speech_recognition pyaudio
```

### Audio Not Working
- Check microphone permissions
- Test with different audio devices
- Restart the application

### Speech Recognition Issues
- Check internet connection
- Speak clearly and slowly
- Try typing instead of speaking

## 📦 Production Deployment

For production deployment, see [DEPLOYMENT.md](DEPLOYMENT.md)

### Create Standalone Executable
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "AI_Agent" main.py
```

### Docker Deployment
```bash
docker build -t ai-agent .
docker run -it --device /dev/snd ai-agent
```

## 🎤 Features

- **Japanese Voice**: Female voice speaks in Japanese
- **Speech Recognition**: Understands Japanese speech
- **Smart Responses**: Context-aware conversation
- **Visual Feedback**: Voice visualization during speech
- **Volume Control**: Adjustable audio levels
- **Conversation History**: Full chat log display
- **Manual Input**: Type messages if speech fails

## 📞 Conversation Script

The bot follows a rice sales script:
1. Introduces as "高木 from X商事"
2. Explains rice business for bento shops
3. Presents "近江ブレンド米・小粒タイプ" product
4. Mentions pricing (588円 per kg)
5. Highlights small grain benefits
6. Offers free samples

## 🛠️ Advanced Configuration

Set environment variables for production:
```bash
export PRODUCTION_MODE=True
export DEFAULT_VOLUME=0.8
export DEFAULT_VOICE_RATE=150
python main.py
```

## 📁 Project Structure

```
AI-free-talking/
├── ai_agent/           # Main application package
├── main.py            # Application entry point
├── run.py             # Smart launcher
├── start_ai_agent.bat # Windows launcher
├── start_ai_agent.sh  # Linux/macOS launcher
├── requirements.txt   # Dependencies
├── DEPLOYMENT.md      # Production guide
└── Readme.md          # Full documentation
```

## 🆘 Need Help?

1. Check the [DEPLOYMENT.md](DEPLOYMENT.md) for detailed setup
2. Read the [Readme.md](Readme.md) for full documentation
3. Check the console output for error messages
4. Ensure all dependencies are installed correctly

---

**Ready to start? Just run the appropriate launcher script for your system!** 🎉
