"""
Speech to Text Module for AI Agent
Uses Python speech recognition to convert spoken words to text
"""

import speech_recognition as sr
import sys
import json

class SpeechToText:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Adjust for ambient noise
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
    
    def listen_for_speech(self, timeout=None):
        """
        Listen for speech and convert it to text
        """
        try:
            print("Listening for speech...", file=sys.stderr)
            
            # Listen for audio
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=timeout)
            
            print("Audio captured, processing...", file=sys.stderr)
            
            # Use Google's speech recognition
            text = self.recognizer.recognize_google(audio)
            print(f"SPEECH:{text}")
            return text
            
        except sr.WaitTimeoutError:
            print("Listening timeout", file=sys.stderr)
            return None
        except sr.UnknownValueError:
            print("Could not understand audio", file=sys.stderr)
            return None
        except sr.RequestError as e:
            print(f"Error with speech recognition service: {e}", file=sys.stderr)
            return None
        except Exception as e:
            print(f"Error in speech recognition: {e}", file=sys.stderr)
            return None

    def continuously_listen(self):
        """
        Continuously listen for speech until interrupted
        """
        print("Starting continuous listening mode. Press Ctrl+C to stop.", file=sys.stderr)
        
        try:
            while True:
                text = self.listen_for_speech(timeout=5)  # Listen for 5 seconds at a time
                if text:
                    print(f"SPEECH:{text}")
                    sys.stdout.flush()  # Ensure output is sent immediately
        except KeyboardInterrupt:
            print("\nStopping speech recognition...", file=sys.stderr)

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "continuous":
        # Continuous listening mode
        stt = SpeechToText()
        stt.continuously_listen()
    else:
        # Single recognition mode
        stt = SpeechToText()
        text = stt.listen_for_speech(timeout=5)
        if text:
            print(f"SPEECH:{text}")
        else:
            print("No speech detected")

if __name__ == "__main__":
    main()