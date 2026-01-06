"""
Python Speech Bridge for AI Agent
This script provides a bridge between the JavaScript application and the Python speech system
"""

import sys
import json
import pyttsx3
import subprocess
import os

# Add the speech_system directory to the Python path to import the existing system
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../speech_system'))

try:
    from talking_module import AgentSpeechSystem
except ImportError:
    print("Error: Could not import the existing speech system.")
    print("Make sure the speech_system directory exists and contains talking_module.py")
    sys.exit(1)

class PythonSpeechBridge:
    def __init__(self):
        self.speech_system = AgentSpeechSystem()
    
    def speak_text(self, text):
        """Speak the provided text using the speech system"""
        self.speech_system.speak(text)
        return {"status": "success", "message": f"Spoke: {text}"}
    
    def get_response(self, text_type):
        """Get a random response of the specified type from the speech patterns"""
        response = self.speech_system.get_random_response(text_type)
        return {"status": "success", "response": response}
    
    def run_demo(self):
        """Run the speech system demo"""
        self.speech_system.simulate_conversation()
        self.speech_system.demo_tone_variations()
        return {"status": "success", "message": "Demo completed"}

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No command provided"}))
        sys.exit(1)
    
    command = sys.argv[1]
    bridge = PythonSpeechBridge()
    
    try:
        if command == "speak":
            if len(sys.argv) < 3:
                print(json.dumps({"error": "No text provided for speaking"}))
                sys.exit(1)
            text = " ".join(sys.argv[2:])
            result = bridge.speak_text(text)
            print(json.dumps(result))
        
        elif command == "get_response":
            if len(sys.argv) < 3:
                print(json.dumps({"error": "No response type provided"}))
                sys.exit(1)
            response_type = sys.argv[2]
            result = bridge.get_response(response_type)
            print(json.dumps(result))
        
        elif command == "demo":
            result = bridge.run_demo()
            print(json.dumps(result))
        
        else:
            print(json.dumps({"error": f"Unknown command: {command}"}))
    
    except Exception as e:
        print(json.dumps({"error": str(e)}))

if __name__ == "__main__":
    main()