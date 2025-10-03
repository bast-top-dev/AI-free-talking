# AI Agent - Production Deployment Guide

## Quick Start (Development)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python main.py
```

## Production Deployment Options

### Option 1: Standalone Executable (Recommended for Windows)

#### Using PyInstaller
1. Install PyInstaller:
```bash
pip install pyinstaller
```

2. Create executable:
```bash
pyinstaller --onefile --windowed --name "AI_Agent" main.py
```

3. The executable will be created in `dist/` folder

#### Using Auto-py-to-exe (GUI Method)
1. Install auto-py-to-exe:
```bash
pip install auto-py-to-exe
```

2. Run the GUI:
```bash
auto-py-to-exe
```

3. Configure:
   - Script Location: `main.py`
   - Onefile: Yes
   - Window Based: Yes
   - Additional Files: Include the `ai_agent` folder

### Option 2: Docker Container

#### Create Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies for audio
RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    python3-pyaudio \
    espeak \
    espeak-data \
    libespeak1 \
    libespeak-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 aiagent && chown -R aiagent:aiagent /app
USER aiagent

# Expose port (if needed for web interface)
EXPOSE 8000

# Run the application
CMD ["python", "main.py"]
```

#### Build and Run Docker Container
```bash
# Build the image
docker build -t ai-agent .

# Run the container
docker run -it --device /dev/snd ai-agent
```

### Option 3: System Service (Linux/macOS)

#### Create systemd service file
```ini
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

#### Install as service
```bash
# Copy files to system directory
sudo cp -r . /opt/ai-agent/
sudo chown -R aiagent:aiagent /opt/ai-agent/

# Install and start service
sudo cp ai-agent.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable ai-agent
sudo systemctl start ai-agent
```

### Option 4: Virtual Environment (Recommended for Server)

#### Create and activate virtual environment
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

## Production Configuration

### Environment Variables
Create a `.env` file:
```env
# Application Settings
APP_TITLE=AI エージェント - 電話営業ボット
LOG_LEVEL=INFO
DEBUG_MODE=False

# Speech Settings
DEFAULT_VOLUME=0.8
DEFAULT_VOICE_RATE=150
SPEECH_TIMEOUT=5

# Conversation Settings
MAX_HISTORY_LENGTH=1000
AUTO_SAVE_INTERVAL=300
```

### Logging Configuration
Add to `main.py`:
```python
import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ai_agent.log'),
        logging.StreamHandler()
    ]
)
```

### Error Handling
Add global exception handler:
```python
import sys
import logging

def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    
    logging.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = handle_exception
```

## Performance Optimization

### 1. Audio Processing
- Use separate threads for audio processing
- Implement audio buffering
- Optimize microphone sensitivity

### 2. Memory Management
- Clear conversation history periodically
- Implement garbage collection
- Monitor memory usage

### 3. Network Optimization
- Cache speech recognition results
- Implement offline mode
- Use local TTS when possible

## Security Considerations

### 1. Input Validation
- Validate all user inputs
- Sanitize text inputs
- Limit conversation length

### 2. Data Privacy
- Don't store sensitive conversation data
- Implement data encryption
- Add user consent mechanisms

### 3. System Security
- Run with minimal privileges
- Validate file paths
- Implement rate limiting

## Monitoring and Maintenance

### 1. Health Checks
```python
def health_check():
    """Check if all components are working."""
    checks = {
        'microphone': test_microphone(),
        'speakers': test_speakers(),
        'internet': test_internet_connection(),
        'tts_engine': test_tts_engine()
    }
    return all(checks.values())
```

### 2. Logging
- Monitor application logs
- Set up log rotation
- Implement alerting for errors

### 3. Updates
- Implement auto-update mechanism
- Backup configuration files
- Test updates in staging environment

## Troubleshooting

### Common Issues

1. **Audio not working**
   - Check microphone permissions
   - Verify audio drivers
   - Test with different audio devices

2. **Speech recognition fails**
   - Check internet connection
   - Verify API keys
   - Test with different languages

3. **Application crashes**
   - Check logs for errors
   - Verify all dependencies
   - Test with minimal configuration

### Debug Mode
Enable debug mode by setting environment variable:
```bash
export DEBUG_MODE=True
python main.py
```

## Scaling Considerations

### For Multiple Users
- Implement user sessions
- Add authentication
- Use database for conversation storage

### For High Volume
- Implement load balancing
- Use message queues
- Add caching mechanisms

### For Cloud Deployment
- Use container orchestration (Kubernetes)
- Implement auto-scaling
- Add monitoring and alerting
