# AI Agent - Alexa-like Voice Assistant

This project implements an AI agent similar to Alexa with voice recognition and response capabilities.

## Architecture

The AI agent consists of several key components:

### 1. Voice Recognition System
- **Voice Recognition Module** (`src/voice/voice_recognition.js`): Handles audio input and converts speech to text
- **Speech-to-Text Bridge** (`src/voice/speech_to_text.py`): Python-based speech recognition using Google's API

### 2. AI Response Processing
- **Response Processor** (`src/ai/response_processor.js`): Processes user input and generates appropriate responses
- Implements intent detection for various command types (greetings, time, date, jokes, etc.)

### 3. Speech Synthesis
- **Speech Bridge** (`src/voice/python_speech_bridge.py`): Connects JavaScript app to Python speech system
- **Speech System Interface** (`src/voice/speech_system.js`): JavaScript wrapper for Python speech
- Leverages existing speech system from `speech_system/talking_module.py`

### 4. Main Application
- **AIAgent** (`index.js`): Main application server using Express and Socket.IO
- Provides real-time communication between frontend and backend
- Integrates all components into a cohesive system

### 5. Frontend Interface
- **Web Interface** (`public/index.html`): HTML/CSS/JavaScript interface for testing
- Allows both voice and text-based interaction
- Displays conversation history in chat format

## Features

- Voice command recognition
- Natural language processing for various intents
- Text-to-speech responses
- Web-based interface for interaction
- Simulated voice recognition for testing
- Context-aware responses

## How It Works

1. User speaks or types a command
2. Voice recognition captures and converts speech to text
3. AI response processor analyzes the input and determines intent
4. Appropriate response is generated based on the detected intent
5. Response is converted to speech and played back to the user
6. Conversation history is maintained for context

## Technologies Used

- Node.js/JavaScript for the main application server
- Python for speech recognition and synthesis
- Socket.IO for real-time communication
- Express for web server functionality
- HTML/CSS/JavaScript for the frontend

## Usage

To start the AI agent:

```bash
node index.js
```

Then navigate to `http://localhost:3000` in your browser to interact with the AI agent.

## Components Integration

The system integrates multiple components:
- Frontend interface communicates via Socket.IO
- Voice recognition bridges JavaScript and Python
- Speech synthesis uses existing Python talking module
- AI processing handles intent detection and response generation

This creates a complete AI agent system similar to Alexa, with voice input, intelligent processing, and voice output capabilities.