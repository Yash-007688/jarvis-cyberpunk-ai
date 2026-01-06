#!/usr/bin/env python3
"""
JARVIS-Style Lab Interface with API Integration
A cyberpunk terminal interface with fixed HUD zones and API connectivity
"""

import time
import random
import psutil
import os
import sys
import requests
import json
from datetime import datetime
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.box import ROUNDED
from rich import print as rprint
import colorama
from colorama import Fore, Back, Style

# Try to import speech functionality
try:
    import win32com.client
    speech_available = True
except ImportError:
    speech_available = False
    print("Warning: pywin32 not installed. Voice output will be disabled.")
    print("To enable voice, install with: pip install pywin32")

# Add backend directory to path to import existing systems
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
if backend_path not in sys.path:
    sys.path.append(backend_path)

# Add speech system directory to path
speech_path = os.path.join(os.path.dirname(__file__), 'speech_system')
if speech_path not in sys.path:
    sys.path.append(speech_path)

try:
    from config import brain_config, get_openrouter_api_key, get_model_config
    backend_available = True
except ImportError:
    backend_available = False
    print("Warning: Backend config not available. Using fallback API.")

try:
    from talking_module import AgentSpeechSystem
    speech_system_available = True
except ImportError:
    speech_system_available = False
    print("Warning: Speech system not available. Using basic TTS.")

# Initialize colorama
colorama.init()
console = Console()

class JARVISLabInterface:
    def __init__(self):
        self.camera_status = "OFF"  # OFF, STANDBY, ACTIVE
        self.ai_core_messages = [
            "JARVIS ONLINE. READY FOR COMMANDS.",
            "SECURITY PROTOCOLS ACTIVE.",
            "NEURAL NETWORKS OPERATIONAL.",
            "SCANNING FOR THREATS...",
            "SYSTEM STATUS: OPTIMAL.",
            "DATA ANALYSIS COMPLETE.",
            "FIREWALL: MAXIMUM SECURITY.",
            "MONITORING ALL SYSTEMS."
        ]
        self.data_stream = []
        self.command_history = []
        self.ai_response = "JARVIS SYSTEM READY. AWAITING COMMANDS."
        self.running = True
        self.api_key = os.getenv("OPENROUTER_API_KEY", "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")
        self.model = os.getenv("MODEL_NAME", "openrouter/auto")
        # Memory system for storing conversation context
        self.conversation_memory = []
        self.max_memory_size = 50  # Keep last 50 interactions
        
        # OS access capabilities
        self.os_access_enabled = True
        
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def call_openrouter_api(self, user_input):
        """Call OpenRouter API to get AI response"""
        try:
            # Use backend config if available, otherwise fallback
            if backend_available:
                api_key = get_openrouter_api_key()
                model_config = get_model_config()
                model = model_config['model']
                temperature = model_config['temperature']
                max_tokens = model_config['max_tokens']
                top_p = model_config['top_p']
            else:
                api_key = self.api_key
                model = self.model
                temperature = 0.7
                max_tokens = 2048
                top_p = 0.9
            
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": model,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an AI assistant that provides helpful, accurate, and concise responses. You understand and respond to queries in English, Hindi, and Hinglish (mixed Hindi-English). Keep responses under 100 words unless specifically asked for more detail. Be conversational and friendly."
                    },
                    {
                        "role": "user",
                        "content": user_input
                    }
                ],
                "temperature": temperature,
                "max_tokens": max_tokens,
                "top_p": top_p
            }
            
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                return f"API Error: {response.status_code} - {response.text}"
                
        except Exception as e:
            print(f"API Error: {str(e)}")
            return self.get_fallback_response(user_input)
    
    def get_fallback_response(self, user_input):
        """Fallback response if API fails"""
        fallback_responses = {
            "hello": ["Hello! How can I assist you today?", "Hi there! What can I do for you?", "Greetings! How may I help you?"],
            "hi": ["Hello! How can I assist you today?", "Hi there! What can I do for you?", "Greetings! How may I help you?"],
            "time": [f"The current time is {datetime.now().strftime('%H:%M:%S')}."],
            "date": [f"Today's date is {datetime.now().strftime('%Y-%m-%d')}."],
            "help": ["I'm your AI assistant! I can help with various tasks. Just ask me a question or give me a command."],
            "default": [f"I understand you're asking about '{user_input}'. How can I assist you further?", 
                       f"Thanks for your input: '{user_input}'. Is there something specific you'd like help with?",
                       f"I've received your message about '{user_input}'. How can I be of service?"]
        }
        
        user_lower = user_input.lower()
        if "hello" in user_lower or "hi" in user_lower:
            return random.choice(fallback_responses["hello"])
        elif "time" in user_lower:
            return random.choice(fallback_responses["time"])
        elif "date" in user_lower:
            return random.choice(fallback_responses["date"])
        elif "help" in user_lower:
            return random.choice(fallback_responses["help"])
        else:
            return random.choice(fallback_responses["default"])
    
    def boot_sequence(self):
        """Simulate JARVIS boot sequence"""
        self.clear_screen()
        
        # Boot sequence with delays
        boot_steps = [
            "INITIALIZING JARVIS LAB SYSTEMS...",
            "LOADING NEURAL NETWORKS...",
            "ACTIVATING SECURITY PROTOCOLS...",
            "CALIBRATING SENSORS...",
            "JARVIS CORE LOADING...",
            "NEURAL INTERFACE ONLINE...",
            "API CONNECTION ESTABLISHED...",
            "ALL SYSTEMS OPERATIONAL."
        ]
        
        for i, step in enumerate(boot_steps):
            self.clear_screen()
            
            # Draw header
            print(Fore.CYAN + Style.BRIGHT + "=" * 80)
            print(Fore.MAGENTA + Style.BRIGHT + "JARVIS LAB INTERFACE v3.0")
            print(Fore.CYAN + Style.BRIGHT + "=" * 80 + Style.RESET_ALL)
            
            # Draw boot progress
            print(Fore.GREEN + Style.BRIGHT + "\nSYSTEM BOOT SEQUENCE")
            print(Fore.CYAN + "-" * 40 + Style.RESET_ALL)
            
            for j, boot_step in enumerate(boot_steps):
                if j < i:
                    print(Fore.GREEN + f"✓ {boot_step}" + Style.RESET_ALL)
                elif j == i:
                    print(Fore.YELLOW + f"▶ {boot_step}" + Style.RESET_ALL)
                else:
                    print(Fore.RED + f"  {boot_step}" + Style.RESET_ALL)
            
            time.sleep(0.7)
        
        # Final boot message
        self.clear_screen()
        print(Fore.CYAN + Style.BRIGHT + "=" * 80)
        print(Fore.MAGENTA + Style.BRIGHT + "JARVIS LAB INTERFACE v3.0")
        print(Fore.CYAN + Style.BRIGHT + "=" * 80 + Style.RESET_ALL)
        
        print(Fore.GREEN + Style.BRIGHT + "\nJARVIS SYSTEM ONLINE" + Style.RESET_ALL)
        print(Fore.CYAN + "Ready for commands. Type 'help' for available commands." + Style.RESET_ALL)
        time.sleep(1.5)
    
    def draw_interface(self):
        """Draw the complete interface with fixed zones"""
        # Fixed panel heights
        top_panel_height = 5  # Camera and System Stats panels
        ai_core_height = 6   # AI Core panel
        bottom_panel_height = 7  # Data Stream and Command Module panels
        
        # Top row: Camera HUD (left) and System Stats (right)
        # Both panels must have the same height (top_panel_height)
        for i in range(top_panel_height):
            if i == 0:
                # Top border
                left_part = "┌─ CAMERA SUBSYSTEM ──────────────────┐"
                right_part = "┌─ SYSTEM STATS ────────────────────┐"
            elif i == 1:
                # Status line
                left_part = f"│ Status: {self.camera_status:<15}{' ' * (14-len(self.camera_status))}│"
                right_part = "│ CPU:  0.0%                     │"
            elif i == 2:
                # Indicator line
                if self.camera_status == "STANDBY":
                    indicator = "●" if int(time.time() * 2) % 2 else "○"
                elif self.camera_status == "ACTIVE":
                    indicator = "●"
                else:
                    indicator = "○"
                left_part = f"│ Indicator: {indicator}                      │"
                right_part = "│ ░░░░░░░░░░░░░░░░░░░│"
            elif i == 3:
                # RAM line
                left_part = "│                                   │"
                right_part = "│ RAM:  0.0%                     │"
            elif i == 4:
                # Bottom border
                left_part = "└────────────────────────────────────┘"
                right_part = "│ ░░░░░░░░░░░░░░░░░░░│"
            
            # Ensure both panels have same height by filling with empty space if needed
            if i < 5:  # Only print for the main 5-line panels
                print(Fore.CYAN + left_part + Fore.MAGENTA + right_part + Style.RESET_ALL)
        
        # Additional lines for system stats (static display)
        print(Fore.MAGENTA + "│ DISK: 0.0%                     │")
        print(Fore.MAGENTA + "│ ░░░░░░░░░░░░░░░░░░░│")
        print(Fore.MAGENTA + f"│ TIME:{datetime.now().strftime('%H:%M:%S')}                     │")
        print(Fore.MAGENTA + "└──────────────────────────────────┘" + Style.RESET_ALL)
        
        # Center: AI Core Display (fixed height)
        print(Fore.GREEN + "┌─ AI CORE ──────────────────────────────────────────────────────────────────┐")
        print(Fore.GREEN + f"│ {Fore.CYAN}{self.ai_response[:74]:<74}{Fore.GREEN}│")
        print(Fore.GREEN + "├─────────────────────────────────────────────────────────────────────────┤")
        
        # Show data stream in the middle section
        for i in range(3):
            if i < len(self.data_stream):
                line = self.data_stream[i][:72]
                print(Fore.GREEN + f"│ {Fore.MAGENTA}{line:<72}{Fore.GREEN}│")
            else:
                print(Fore.GREEN + f"│ {' ':<72}{Fore.GREEN}│")
        
        print(Fore.GREEN + "└─────────────────────────────────────────────────────────────────────────┘" + Style.RESET_ALL)
        
        # Bottom row: Data Stream (left) and Command Module (right)
        # Both panels must have the same height (bottom_panel_height)
        for i in range(bottom_panel_height):
            if i == 0:
                # Top border
                left_part = "┌─ DATA STREAM ──────────────────┐"
                right_part = "┌─ COMMAND MODULE ──────────────┐"
            elif i < 6:
                # Content lines
                if i-1 < len(self.data_stream):
                    data_line = self.data_stream[i-1][-28:]  # Show last 28 chars to fit
                    left_part = f"│ {data_line:<28}│"
                else:
                    # Generate random matrix-style data
                    if random.random() < 0.3:
                        matrix_data = ''.join([random.choice('01') for _ in range(10)])
                        left_part = f"│ {matrix_data:<28}│"
                    else:
                        left_part = f"│ {' ':<28}│"
                
                right_part = f"│ {' ':<28}│"
            else:
                # Bottom border
                left_part = "└───────────────────────────────┘"
                right_part = "└───────────────────────────────┘"
            
            print(Fore.CYAN + left_part + Fore.MAGENTA + right_part + Style.RESET_ALL)
        
        # Print command prompt at the very bottom
        print(Fore.CYAN + f"\n[JARVIS] Enter command: " + Style.RESET_ALL, end='')
    
    def type_text(self, text, delay=0.02):
        """Simulate typing effect for AI responses"""
        for char in text:
            print(Fore.CYAN + char, end='', flush=True)
            time.sleep(delay)
        print(Style.RESET_ALL)
    
    def process_command(self, command):
        """Process user commands"""
        cmd = command.lower().strip()
        
        # Add command to memory
        self.add_to_memory("user", command)
        
        if cmd == "help":
            response = "AVAILABLE COMMANDS: camera on, camera off, camera standby, status, help, api test, os info, list files, memory show, memory clear, shutdown, restart"
        elif cmd == "status":
            cpu = psutil.cpu_percent()
            mem = psutil.virtual_memory().percent
            response = f"SYSTEM STATUS: CPU {cpu}%, RAM {mem}%, CAMERA {self.camera_status}"
        elif cmd == "camera on":
            self.camera_status = "ACTIVE"
            response = "CAMERA SUBSYSTEM ACTIVATED. LIVE FEED ACTIVE."
        elif cmd == "camera off":
            self.camera_status = "OFF"
            response = "CAMERA SUBSYSTEM DEACTIVATED."
        elif cmd == "camera standby":
            self.camera_status = "STANDBY"
            response = "CAMERA SUBSYSTEM IN STANDBY MODE."
        elif cmd == "api test":
            response = self.call_openrouter_api("Hello, how are you?")
        elif cmd == "os info":
            response = self.get_os_info()
        elif cmd.startswith("list files"):
            path = cmd.split(" ", 2)[2] if len(cmd.split(" ")) > 2 else "./"
            response = self.list_directory(path)
        elif cmd == "memory show":
            response = self.show_memory()
        elif cmd == "memory clear":
            self.clear_memory()
            response = "CONVERSATION MEMORY CLEARED."
        elif cmd == "shutdown":
            response = "SHUTTING DOWN JARVIS SYSTEM..."
            self.running = False
        elif cmd == "restart":
            response = "RESTARTING JARVIS SYSTEM..."
            os.execv(sys.executable, ['python'] + sys.argv)
        elif cmd == "":
            response = "AWAITING COMMAND INPUT."
        else:
            # Process as API request with memory context
            response = self.call_openrouter_api_with_memory(command)
        
        self.ai_response = response
        self.command_history.append(command)
        
        # Add response to memory
        self.add_to_memory("ai", response)
        
        # Add response to data stream
        self.data_stream.append(f"[{datetime.now().strftime('%H:%M:%S')}] {response[:50]}")
        if len(self.data_stream) > 10:
            self.data_stream.pop(0)
        
        # Speak the response if speech is available
        self.speak_response(response)
    
    def add_to_memory(self, role, message):
        """Add conversation to memory"""
        self.conversation_memory.append({
            "role": role,
            "message": message,
            "timestamp": datetime.now().strftime('%H:%M:%S')
        })
        
        # Keep memory size manageable
        if len(self.conversation_memory) > self.max_memory_size:
            self.conversation_memory.pop(0)
    
    def get_os_info(self):
        """Get operating system information"""
        import platform
        os_name = platform.system()
        os_version = platform.version()
        os_release = platform.release()
        machine = platform.machine()
        processor = platform.processor()
        
        return f"OS: {os_name} {os_release} ({os_version}) | Machine: {machine} | Processor: {processor}"
    
    def list_directory(self, path):
        """List directory contents"""
        try:
            if os.path.exists(path):
                items = os.listdir(path)
                if not items:
                    return f"Directory '{path}' is empty."
                else:
                    return f"Contents of '{path}': {', '.join(items[:20])}"  # Show first 20 items
            else:
                return f"Directory '{path}' does not exist."
        except Exception as e:
            return f"Error accessing directory: {str(e)}"
    
    def show_memory(self):
        """Show conversation memory"""
        if not self.conversation_memory:
            return "No conversation memory available."
        
        memory_str = f"Memory contains {len(self.conversation_memory)} interactions:\n"
        for i, entry in enumerate(self.conversation_memory[-5:], 1):  # Show last 5 entries
            role = "USER" if entry['role'] == 'user' else "JARVIS"
            memory_str += f"[{entry['timestamp']}] {role}: {entry['message'][:30]}{'...' if len(entry['message']) > 30 else ''}\n"
        return memory_str
    
    def clear_memory(self):
        """Clear conversation memory"""
        self.conversation_memory = []
    
    def call_openrouter_api_with_memory(self, user_input):
        """Call OpenRouter API with conversation memory context"""
        try:
            # Use backend config if available, otherwise fallback
            if backend_available:
                api_key = get_openrouter_api_key()
                model_config = get_model_config()
                model = model_config['model']
                temperature = model_config['temperature']
                max_tokens = model_config['max_tokens']
                top_p = model_config['top_p']
            else:
                api_key = self.api_key
                model = self.model
                temperature = 0.7
                max_tokens = 2048
                top_p = 0.9
            
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            # Build context from memory
            messages = [
                {
                    "role": "system",
                    "content": "You are JARVIS, an advanced AI assistant with OS access capabilities. You understand and respond to queries in English, Hindi, and Hinglish. Keep responses under 100 words unless specifically asked for more detail. Be conversational and friendly. Use the conversation history for context."
                }
            ]
            
            # Add recent conversation history
            for entry in self.conversation_memory[-5:]:  # Use last 5 interactions as context
                role = "user" if entry['role'] == 'user' else "assistant"
                messages.append({
                    "role": role,
                    "content": entry['message']
                })
            
            # Add the current user input
            messages.append({
                "role": "user",
                "content": user_input
            })
            
            data = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "top_p": top_p
            }
            
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                return f"API Error: {response.status_code} - {response.text}"
                
        except Exception as e:
            print(f"API Error: {str(e)}")
            return self.get_fallback_response(user_input)
    
    def speak_response(self, text):
        """Speak the response using the enhanced speech system"""
        global speech_available, speech_system_available
        
        if speech_system_available:
            # Use the enhanced speech system
            try:
                if not hasattr(self, 'agent_speech_system'):
                    self.agent_speech_system = AgentSpeechSystem()
                self.agent_speech_system.speak(text, use_voice=True)
            except Exception as e:
                print(f"Enhanced speech error: {e}")
                # Fallback to basic speech if enhanced fails
                if speech_available:
                    try:
                        speaker = win32com.client.Dispatch("SAPI.SpVoice")
                        speaker.Speak(text)
                    except Exception as e2:
                        print(f"Basic speech error: {e2}")
        elif speech_available:
            # Use basic Windows SAPI
            try:
                speaker = win32com.client.Dispatch("SAPI.SpVoice")
                speaker.Speak(text)
            except Exception as e:
                print(f"Speech error: {e}")
        else:
            # If speech is not available, just show a message
            pass
    
    def run_interface(self):
        """Main interface loop"""
        self.boot_sequence()
        
        while self.running:
            try:
                self.clear_screen()
                
                # Update system stats in real-time
                self.draw_interface()
                
                # Get user input
                user_input = input()
                
                if user_input.lower() in ['exit', 'quit', 'q']:
                    print(Fore.RED + "[JARVIS] SHUTTING DOWN SYSTEMS..." + Style.RESET_ALL)
                    break
                
                # Process the command
                self.process_command(user_input)
                
                # Brief pause to show the result
                time.sleep(0.5)
                
            except KeyboardInterrupt:
                print(Fore.RED + "\n[JARVIS] SYSTEM INTERRUPT. SHUTTING DOWN..." + Style.RESET_ALL)
                break
            except Exception as e:
                print(Fore.RED + f"[ERROR] {str(e)}" + Style.RESET_ALL)
                time.sleep(2)

def main():
    """Main function to run the JARVIS lab interface"""
    jarvis = JARVISLabInterface()
    jarvis.run_interface()

if __name__ == "__main__":
    main()