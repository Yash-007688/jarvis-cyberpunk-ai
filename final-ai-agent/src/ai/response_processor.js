/**
 * AI Response Processing System
 * Processes user input and generates appropriate AI responses using OpenRouter API
 */

const { AgentSpeechSystem } = require('../voice/speech_system');
const OpenAI = require('openai');

class ResponseProcessor {
    constructor() {
        this.speechSystem = new AgentSpeechSystem();
        this.context = {}; // Store conversation context
        
        // Initialize OpenAI client with OpenRouter configuration
        this.openai = new OpenAI({
            baseURL: "https://openrouter.ai/api/v1",
            apiKey: process.env.OPENROUTER_API_KEY || "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",
        });
        
        this.model = process.env.MODEL_NAME || "openrouter/auto";
        this.temperature = parseFloat(process.env.MODEL_TEMPERATURE || 0.7);
        this.maxTokens = parseInt(process.env.MODEL_MAX_TOKENS || 2048);
        
        // Initialize with default intent matchers but will use AI for most responses
        this.intentMatchers = this.initializeIntentMatchers();
    }

    /**
     * Initialize intent matchers for understanding user commands
     */
    initializeIntentMatchers() {
        return [
            // Greeting intents
            {
                name: 'greeting',
                patterns: [
                    /\b(hello|hi|hey|greetings|good morning|good afternoon|good evening)\b/i,
                ],
                handler: this.handleGreeting.bind(this)
            },
            // Time intents
            {
                name: 'time',
                patterns: [
                    /\b(what time|time is it|current time|tell me the time|what's the time)\b/i,
                    /\b(time|clock)\b/i,
                ],
                handler: this.handleTime.bind(this)
            },
            // Date intents
            {
                name: 'date',
                patterns: [
                    /\b(what date|date is it|current date|tell me the date|what's the date|today's date)\b/i,
                    /\b(date|today)\b/i,
                ],
                handler: this.handleDate.bind(this)
            },
            // Weather intents
            {
                name: 'weather',
                patterns: [
                    /\b(weather|temperature|hot|cold|rain|sunny|forecast)\b/i,
                ],
                handler: this.handleWeather.bind(this)
            },
            // Joke intents
            {
                name: 'joke',
                patterns: [
                    /\b(tell me a joke|make me laugh|funny|joke|humor)\b/i,
                ],
                handler: this.handleJoke.bind(this)
            },
            // Music intents
            {
                name: 'music',
                patterns: [
                    /\b(play music|music|song|playlist|start music)\b/i,
                ],
                handler: this.handleMusic.bind(this)
            },
            // Help intents
            {
                name: 'help',
                patterns: [
                    /\b(help|assist|support|what can you do|how can you help)\b/i,
                ],
                handler: this.handleHelp.bind(this)
            },
            // General query intents
            {
                name: 'general',
                patterns: [
                    /\b(how are you|how do you work|what are you|who are you|what can you do)\b/i,
                ],
                handler: this.handleGeneral.bind(this)
            }
        ];
    }

    /**
     * Process user input and generate a response
     * @param {string} userInput - The user's input text
     * @returns {string} - The AI-generated response
     */
    async processInput(userInput) {
        try {
            console.log('Processing input:', userInput); // Debug logging
            
            // Use OpenRouter API to generate response
            const completion = await this.openai.chat.completions.create({
                model: this.model,
                messages: [
                    {
                        role: "system",
                        content: `You are an AI assistant that provides helpful, accurate, and concise responses. You understand and respond to queries in English, Hindi, and Hinglish (mixed Hindi-English). Keep responses under 100 words unless specifically asked for more detail. Be conversational and friendly.`
                    },
                    {
                        role: "user",
                        content: userInput
                    }
                ],
                temperature: this.temperature,
                max_tokens: this.maxTokens,
                top_p: parseFloat(process.env.MODEL_TOP_P || 0.9),
            });
            
            const response = completion.choices[0].message.content;
            console.log('API Response:', response); // Debug logging
            return response;
        } catch (error) {
            console.error('Error calling OpenRouter API:', error);
            
            // Fallback to original behavior if API fails
            const normalizedInput = userInput.toLowerCase().trim();
            
            // Try to match intents
            for (const matcher of this.intentMatchers) {
                for (const pattern of matcher.patterns) {
                    if (pattern.test(normalizedInput)) {
                        const response = matcher.handler(normalizedInput);
                        console.log('Intent matched, response:', response); // Debug logging
                        return response;
                    }
                }
            }
            
            // If no specific intent matched, provide a general response
            const response = this.handleGeneral(normalizedInput);
            console.log('General response:', response); // Debug logging
            return response;
        }
    }

    /**
     * Handle greeting intents
     */
    handleGreeting(input) {
        const greetings = [
            "Hello! How can I assist you today?",
            "Hi there! What can I do for you?",
            "Greetings! How may I help you?",
            "Hey! What can I help you with?"
        ];
        return greetings[Math.floor(Math.random() * greetings.length)];
    }

    /**
     * Handle time intents
     */
    handleTime(input) {
        const now = new Date();
        const timeString = now.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
        return `The current time is ${timeString}.`;
    }

    /**
     * Handle date intents
     */
    handleDate(input) {
        const now = new Date();
        const dateString = now.toLocaleDateString([], {weekday: 'long', year: 'numeric', month: 'long', day: 'numeric'});
        return `Today's date is ${dateString}.`;
    }

    /**
     * Handle weather intents (simulated)
     */
    handleWeather(input) {
        const weatherResponses = [
            "I don't have access to real weather data right now, but I can suggest checking a weather app or website.",
            "For accurate weather information, I recommend checking your local weather service.",
            "I'm unable to provide weather data at the moment, but it seems like a nice day!"
        ];
        return weatherResponses[Math.floor(Math.random() * weatherResponses.length)];
    }

    /**
     * Handle joke intents
     */
    handleJoke(input) {
        const jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the scarecrow win an award? He was outstanding in his field!",
            "Why don't eggs tell jokes? They'd crack each other up!",
            "What do you call a fake noodle? An impasta!",
            "Why did the math book look so sad? Because it had too many problems."
        ];
        return jokes[Math.floor(Math.random() * jokes.length)];
    }

    /**
     * Handle music intents (simulated)
     */
    handleMusic(input) {
        const musicResponses = [
            "I'm starting to play some music for you now.",
            "Playing your requested music.",
            "I'll queue up some music for you.",
            "Now playing music as requested."
        ];
        return musicResponses[Math.floor(Math.random() * musicResponses.length)];
    }

    /**
     * Handle help intents
     */
    handleHelp(input) {
        return "I'm your AI assistant! I can help with various tasks like telling the time, sharing jokes, providing information, and more. Just ask me a question or give me a command.";
    }

    /**
     * Handle general queries
     */
    handleGeneral(input) {
        // For more sophisticated processing, we could integrate with NLP services
        // For now, we'll return a general response
        const generalResponses = [
            `I understand you're asking about "${input}". How can I assist you further?`,
            `Thanks for your input: "${input}". Is there something specific you'd like help with?`,
            `I've received your message about "${input}". How can I be of service?`,
            `I'm here to help with various tasks. Could you provide more details about what you need?`
        ];
        return generalResponses[Math.floor(Math.random() * generalResponses.length)];
    }

    /**
     * Update conversation context
     */
    updateContext(key, value) {
        this.context[key] = value;
    }

    /**
     * Get value from conversation context
     */
    getContext(key) {
        return this.context[key];
    }
}

module.exports = { ResponseProcessor };