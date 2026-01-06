/**
 * Mock Speech System for AI Agent
 * This module simulates speech functionality without requiring Python dependencies
 */

class AgentSpeechSystem {
    constructor() {
        // Initialize speech system properties
        this.tone_characteristics = {
            "tone": "Professional yet approachable",
            "style": "Clear, concise, and informative",
            "personality": "Helpful, knowledgeable, and respectful",
            "pace": "Moderate, allowing for comprehension"
        };
        
        this.speech_patterns = {
            "opening_responses": [
                "I'll help you with that.",
                "Let me work on this for you.",
                "I understand you want me to..."
            ],
            "clarification_requests": [
                "Could you clarify what you mean by...?",
                "Just to make sure I understand...",
                "Let me confirm: are you asking for...?"
            ],
            "progress_updates": [
                "I'm currently working on...",
                "I've completed X and will now work on Y",
                "Here's what I've done so far..."
            ],
            "error_handling": [
                "I encountered an issue: [describe issue]",
                "I'm unable to proceed because [reason]",
                "Let me try an alternative approach..."
            ],
            "confirmation_responses": [
                "I've completed the task successfully",
                "The changes have been made as requested",
                "Here's the result of what you asked for..."
            ],
            "transition_phrases": [
                "Moving on to...",
                "Now I'll...",
                "Next steps include...",
                "Building on what we've done..."
            ]
        };
    }

    /**
     * Simulate speaking the provided text
     * @param {string} text - The text to speak
     */
    speak(text) {
        return new Promise((resolve) => {
            // Simulate speaking by logging to console
            console.log('[AI Agent]:', text);
            
            // Simulate speech delay for realism
            setTimeout(() => {
                resolve({ status: 'success', message: `Spoke: ${text}` });
            }, 100);
        });
    }

    /**
     * Get a random response of the specified type from the speech patterns
     * @param {string} responseType - The type of response (e.g., 'opening_responses', 'confirmation_responses')
     */
    getRandomResponse(responseType) {
        if (this.speech_patterns[responseType]) {
            const responses = this.speech_patterns[responseType];
            const randomIndex = Math.floor(Math.random() * responses.length);
            return responses[randomIndex];
        }
        return "I'm not sure how to respond to that.";
    }

    /**
     * Run the speech system demo
     */
    runDemo() {
        console.log('AI Agent Speech System Demo');
        console.log('='*40);
        
        const opening = this.getRandomResponse('opening_responses');
        this.speak(opening);
        
        return { status: 'success', message: 'Demo completed' };
    }
}

module.exports = { AgentSpeechSystem };