# JARVIS Cyberpunk AI Assistant

A futuristic cyberpunk-style AI assistant terminal interface with advanced capabilities including OS access, memory, and speech functionality.

## Features

- **Cyberpunk Terminal Interface**: Futuristic JARVIS-style lab interface with neon aesthetics
- **AI Integration**: Powered by OpenRouter API for intelligent responses
- **OS Access**: Direct access to system information and file operations
- **Memory System**: Conversation history with context awareness
- **Speech System**: Text-to-speech functionality with enhanced voice capabilities
- **Backend Integration**: Connected to existing backend and speech systems
- **Camera Status**: Visual camera status indicators (simulated)
- **Real-time Stats**: System monitoring capabilities

## Architecture

The system integrates multiple components:
- **Frontend**: Terminal-based cyberpunk interface
- **Backend**: OpenRouter API integration with conversation memory
- **Speech**: Enhanced speech system with TTS capabilities
- **OS Access**: Direct system information and file operations

## Commands

- `help` - Show available commands
- `status` - Show system status
- `os info` - Get operating system information
- `list files [path]` - List directory contents
- `memory show` - Show conversation memory
- `memory clear` - Clear conversation memory
- `camera on/off/standby` - Control camera status
- `api test` - Test API connectivity
- `shutdown` - Shut down the system
- `restart` - Restart the system

## Installation

1. Clone the repository
2. Install required Python packages:
   ```bash
   pip install rich colorama psutil requests pywin32
   ```
3. Set up your OpenRouter API key in environment variables
4. Run the interface:
   ```bash
   python jarvis-api-integration.py
   ```

## Requirements

- Python 3.7+
- Windows OS (for speech functionality)
- OpenRouter API key

## License

MIT