import time
import random
import pyttsx3
try:
    import sys
    import os
    # Add backend directory to path to import config
    backend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'backend')
    if backend_path not in sys.path:
        sys.path.append(backend_path)
    
    from config import get_voice_settings
    from dotenv import load_dotenv
    load_dotenv()  # Load environment variables from .env file
except ImportError:
    # If config or python-dotenv is not available, continue with defaults
    get_voice_settings = None

class AgentSpeechSystem:
    def __init__(self):
        self.tone_characteristics = {
            "tone": "Professional yet approachable",
            "style": "Clear, concise, and informative",
            "personality": "Helpful, knowledgeable, and respectful",
            "pace": "Moderate, allowing for comprehension"
        }
        
        self.speech_patterns = {
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
        }
        
        # Initialize text-to-speech engine
        self.engine = pyttsx3.init()
        self.setup_voice_properties()
    
    def setup_voice_properties(self):
        """Configure the voice properties for the speech engine"""
        # Get available voices
        voices = self.engine.getProperty('voices')
        
        # Set the first available voice (usually female on Windows)
        if voices:
            self.engine.setProperty('voice', voices[0].id)
        
        # Use voice settings from config if available, otherwise use defaults
        if get_voice_settings:
            settings = get_voice_settings()
            # Set speech rate (words per minute)
            self.engine.setProperty('rate', settings.get('rate', 180))
            
            # Set volume (0.0 to 1.0)
            self.engine.setProperty('volume', settings.get('volume', 0.9))
        else:
            # Set speech rate (words per minute)
            self.engine.setProperty('rate', 180)  # Default is 200, slightly slower for clarity
            
            # Set volume (0.0 to 1.0)
            self.engine.setProperty('volume', 0.9)

    def speak(self, message, delay=0.05, use_voice=True):
        """Simulate speaking with a delay between characters for realistic effect and optional voice output"""
        # Print the message to console
        for char in message:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()  # New line at the end
        
        # Speak the message using text-to-speech if enabled
        if use_voice:
            self.engine.say(message)
            self.engine.runAndWait()

    def get_random_response(self, response_type):
        """Get a random response from the specified category"""
        if response_type in self.speech_patterns:
            return random.choice(self.speech_patterns[response_type])
        return "I'm not sure how to respond to that."

    def simulate_conversation(self):
        """Simulate a conversation using the speech system"""
        print("AI Agent Speech System Demo")
        print("="*40)
        
        # Opening
        opening = self.get_random_response("opening_responses")
        print("Agent:", end=" ")
        self.speak(opening)
        time.sleep(1)
        
        # Simulate some work
        print("Agent:", end=" ")
        progress = self.get_random_response("progress_updates")
        self.speak(f"{progress} setting up the speech system.")
        time.sleep(1)
        
        # Simulate processing
        print("Agent:", end=" ")
        self.speak("I'm analyzing your request and preparing a response.")
        time.sleep(1)
        
        # Simulate completion
        print("Agent:", end=" ")
        confirmation = self.get_random_response("confirmation_responses")
        self.speak(confirmation)
        time.sleep(1)
        
        # Closing
        print("Agent:", end=" ")
        self.speak("Is there anything else I can help you with today?")
        
    def demo_tone_variations(self):
        """Demonstrate different tone variations"""
        print("\nTone Variations Demo:")
        print("-"*25)
        
        # Professional tone
        print("Professional Context:")
        self.speak("Based on the analysis, the recommended approach would be to implement a modular design pattern.")
        time.sleep(0.5)
        
        # Casual tone
        print("\nCasual Context:")
        self.speak("Sure thing! No problem, I can help with that.")
        time.sleep(0.5)
        
        # Technical tone
        print("\nTechnical Context:")
        self.speak("From a technical standpoint, the implementation involves several key components including data parsing and validation modules.")
        time.sleep(0.5)

def main():
    agent = AgentSpeechSystem()
    
    print("Welcome to the AI Agent Talking Module")
    print("=====================================")
    
    # Run the conversation simulation
    agent.simulate_conversation()
    
    # Demo tone variations
    agent.demo_tone_variations()
    
    # Interactive mode
    print("\nEntering interactive mode...")
    print("Type your message (or 'quit' to exit):")
    
    while True:
        user_input = input(">> ")
        if user_input.lower() in ['quit', 'exit', 'q']:
            agent.speak("Goodbye! Have a great day!")
            break
        elif user_input.strip():
            # Simple response based on keywords
            if any(word in user_input.lower() for word in ['hello', 'hi', 'hey']):
                response = "Hello there! How can I assist you today?"
            elif any(word in user_input.lower() for word in ['help', 'assist', 'support']):
                response = "I'm here to help. What do you need assistance with?"
            elif any(word in user_input.lower() for word in ['name', 'who', 'what']):
                response = "I'm an AI assistant with a professional yet approachable tone."
            else:
                response = f"I understand you're saying: {user_input}. How can I help you further?"
            
            agent.speak(response)
    
    print("\nDemo completed!")

if __name__ == "__main__":
    main()