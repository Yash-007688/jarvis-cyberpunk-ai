// AI Agent - Main Application Entry Point
// This is the main file that starts our Alexa-like AI agent

require('dotenv').config();

const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const fs = require('fs');
const path = require('path');

// Import the speech system, voice recognition, and AI response processor
const { AgentSpeechSystem } = require('./src/voice/speech_system');
const { VoiceRecognition } = require('./src/voice/voice_recognition');
const { ResponseProcessor } = require('./src/ai/response_processor');

class AIAgent {
    constructor() {
        this.app = express();
        this.server = http.createServer(this.app);
        this.io = socketIo(this.server);
        
        this.speechSystem = new AgentSpeechSystem();
        this.voiceRecognition = new VoiceRecognition();
        this.responseProcessor = new ResponseProcessor();
        this.isListening = false;
        this.conversationHistory = [];
        
        this.setupExpress();
        this.setupSocketHandlers();
        this.setupRoutes();
    }
    
    setupExpress() {
        // Serve static files
        this.app.use(express.static(path.join(__dirname, 'public')));
        
        // Parse JSON bodies
        this.app.use(express.json());
    }
    
    setupRoutes() {
        this.app.get('/', (req, res) => {
            res.sendFile(path.join(__dirname, 'public', 'index.html'));
        });
    }
    
    setupSocketHandlers() {
        this.io.on('connection', (socket) => {
            console.log('A user connected');
            
            socket.on('start_listening', () => {
                this.isListening = true;
                this.speechSystem.speak("Hello! I'm your AI assistant. How can I help you today?");
                
                // Set up voice recognition callbacks
                this.voiceRecognition.setCallbacks(
                    (command) => {
                        console.log('Voice command detected:', command);
                        this.processCommand(command, socket);
                    },
                    (error) => {
                        console.error('Voice recognition error:', error);
                        socket.emit('error', { message: error });
                    }
                );
                
                // Start listening for voice commands
                this.voiceRecognition.startListening();
            });
            
            socket.on('voice_command', (data) => {
                this.processCommand(data.command, socket);
            });
            
            socket.on('disconnect', () => {
                console.log('A user disconnected');
            });
        });
    }
    
    async processCommand(command, socket) {
        // Add to conversation history
        this.conversationHistory.push({type: 'user', content: command, timestamp: new Date()});
        
        // Generate response using the AI system
        try {
            let response = await this.generateResponse(command);
            
            // Add to conversation history
            this.conversationHistory.push({type: 'agent', content: response, timestamp: new Date()});
            
            // Send response back to client
            socket.emit('agent_response', { response: response });
            
            // Speak the response using our speech system
            this.speechSystem.speak(response);
        } catch (error) {
            console.error('Error processing command:', error);
            const errorMessage = "Sorry, I encountered an issue processing your request. Please try again.";
            socket.emit('agent_response', { response: errorMessage });
            this.speechSystem.speak(errorMessage);
        }
    }
    
    async generateResponse(command) {
        // Use the AI response processor to generate a response
        return await this.responseProcessor.processInput(command);
    }
    
    start(port = 3000) {
        this.server.listen(port, () => {
            console.log(`AI Agent server listening on port ${port}`);
            this.speechSystem.speak("AI Agent system initialized and ready to assist!");
        });
    }
}

// Initialize and start the AI agent
// Start the AI agent when running directly
if (require.main === module) {
    console.log('Starting AI Agent server...');
    const agent = new AIAgent();
    agent.start();
} else {
    // Export for use as module
    module.exports = AIAgent;
}