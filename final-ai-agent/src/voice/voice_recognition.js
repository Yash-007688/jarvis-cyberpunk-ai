/**
 * Voice Recognition Module for AI Agent
 * Handles audio input and converts speech to text (mock implementation)
 */

class VoiceRecognition {
    constructor() {
        this.isListening = false;
        this.callbacks = {
            onSpeechDetected: null,
            onError: null
        };
        
        // Timer for simulated voice recognition
        this.listenTimer = null;
    }

    /**
     * Set callback functions for speech detection and errors
     * @param {Function} onSpeechDetected - Callback when speech is detected and converted to text
     * @param {Function} onError - Callback when an error occurs
     */
    setCallbacks(onSpeechDetected, onError) {
        this.callbacks.onSpeechDetected = onSpeechDetected;
        this.callbacks.onError = onError;
    }

    /**
     * Start listening for voice input
     */
    startListening() {
        if (this.isListening) {
            console.log('Already listening...');
            return;
        }

        this.isListening = true;
        console.log('Starting voice recognition...');

        // Start simulated voice recognition
        this.simulateListening();
    }

    /**
     * Stop listening for voice input
     */
    stopListening() {
        this.isListening = false;
        if (this.listenTimer) {
            clearTimeout(this.listenTimer);
            this.listenTimer = null;
        }
        console.log('Stopped listening');
    }

    /**
     * Simulate voice recognition (for demo purposes)
     */
    simulateListening() {
        console.log('Voice recognition is now active. Waiting for input...');
        
        // Simulate some possible user commands after a delay
        this.listenTimer = setTimeout(() => {
            if (this.isListening && this.callbacks.onSpeechDetected) {
                // For demo purposes, we'll simulate a voice command
                const simulatedCommands = [
                    "Hello AI assistant",
                    "What time is it?",
                    "Tell me a joke",
                    "How's the weather?",
                    "Play some music",
                    "What can you do?",
                    "Help me with something"
                ];
                
                // Pick a random command for simulation
                const randomCommand = simulatedCommands[Math.floor(Math.random() * simulatedCommands.length)];
                
                console.log(`Simulated voice input detected: "${randomCommand}"`);
                this.callbacks.onSpeechDetected(randomCommand);
                
                // Continue listening for more simulated commands
                if (this.isListening) {
                    this.simulateListening();
                }
            }
        }, 10000); // Simulate command every 10 seconds
    }
}

module.exports = { VoiceRecognition };