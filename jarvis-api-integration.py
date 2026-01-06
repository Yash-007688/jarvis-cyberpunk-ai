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

# Add backend screen monitor to path
screen_monitor_path = os.path.join(os.path.dirname(__file__), 'backend')
if screen_monitor_path not in sys.path:
    sys.path.append(screen_monitor_path)

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

try:
    from screen_monitor import ScreenMonitor
    screen_monitor_available = True
    screen_monitor = ScreenMonitor()
except ImportError:
    screen_monitor_available = False
    print("Warning: Screen monitor not available. Install required packages.")

try:
    from app_launcher import AppLauncher
    app_launcher_available = True
    app_launcher = AppLauncher()
except ImportError:
    app_launcher_available = False
    print("Warning: App launcher not available. Install required packages.")

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
            "🤖 INITIALIZING JARVIS ROBOTIC SYSTEMS...",
            "🤖 LOADING NEURAL NETWORKS...",
            "🤖 ACTIVATING SECURITY PROTOCOLS...",
            "🤖 CALIBRATING SENSORS...",
            "🤖 JARVIS CORE LOADING...",
            "🤖 NEURAL INTERFACE ONLINE...",
            "🤖 API CONNECTION ESTABLISHED...",
            "🤖 ALL SYSTEMS OPERATIONAL."
        ]
        
        for i, step in enumerate(boot_steps):
            self.clear_screen()
            
            # Draw header
            print(Fore.CYAN + Style.BRIGHT + "╔" + "═" * 78 + "╗")
            print(Fore.MAGENTA + Style.BRIGHT + "║" + " " * 27 + "🤖 JARVIS ROBOTIC INTERFACE v3.0" + " " * 27 + "║")
            print(Fore.CYAN + Style.BRIGHT + "╠" + "═" * 78 + "╣" + Style.RESET_ALL)
            
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
        # Get current system stats
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Fixed panel heights
        camera_height = 3
        system_stats_height = 5
        data_stream_height = 10
        chat_height = 15
        
        # Left side: Camera HUD at the top
        print(Fore.CYAN + "┌─ 🤖 CAM ──────┐")
        print(Fore.CYAN + f"│ {self.camera_status[:8]:<8} │")
        print(Fore.CYAN + "└──────────────┘")
        
        # Left side: System Stats below camera
        print(Fore.MAGENTA + "┌─ 🤖 SYS ──────┐")
        print(Fore.MAGENTA + f"│ CPU: {cpu_percent:4.0f}% │")
        print(Fore.MAGENTA + f"│ RAM: {memory.percent:4.0f}% │")
        print(Fore.MAGENTA + f"│ DISK:{(disk.used/disk.total)*100:4.0f}% │")
        print(Fore.MAGENTA + f"│ TIME:{datetime.now().strftime('%H:%M')} │")
        print(Fore.MAGENTA + "└──────────────┘" + Style.RESET_ALL)
        
        # Center: Data Stream panel
        print(Fore.CYAN + "┌─ 🤖 DATA STREAM ──────────────────────────────────────────────────────────┐")
        
        # Show data stream content
        for i in range(data_stream_height - 2):  # -2 for top and bottom borders
            if i < len(self.data_stream):
                line = self.data_stream[i][:76]
                print(Fore.CYAN + f"│ {Fore.MAGENTA}{line:<76}{Fore.CYAN}│")
            else:
                # Generate random matrix-style data
                if random.random() < 0.3:
                    matrix_data = ''.join([random.choice('01') for _ in range(20)])
                    print(Fore.CYAN + f"│ {matrix_data:<76}{Fore.CYAN}│")
                else:
                    print(Fore.CYAN + f"│ {' ':<76}{Fore.CYAN}│")
        
        print(Fore.CYAN + "└─────────────────────────────────────────────────────────────────────────┘" + Style.RESET_ALL)
        
        # Right side: WhatsApp-style Chat Container (extreme right)
        print(Fore.GREEN + "┌─ 💬 CHAT ────────────────────────────────────────────────────────────────┐")
        
        # Show AI responses in WhatsApp-style format
        for i in range(chat_height - 2):  # -2 for top and bottom borders
            if i == 0:
                # Show the current AI response
                ai_msg = f"🤖 JARVIS: {self.ai_response[:62]}" if len(self.ai_response) <= 62 else f"🤖 JARVIS: {self.ai_response[:60]}..."
                print(Fore.GREEN + f"│ {ai_msg:<76}{Fore.GREEN}│")
            elif i == 1:
                # Timestamp
                timestamp = f"⏰ {datetime.now().strftime('%H:%M:%S')}"
                print(Fore.GREEN + f"│ {timestamp:<76}{Fore.GREEN}│")
            else:
                # Show data stream items in chat format
                if i-2 < len(self.data_stream):
                    chat_line = self.data_stream[i-2][:70]
                    print(Fore.GREEN + f"│ 📩 {chat_line:<74}{Fore.GREEN}│")
                else:
                    print(Fore.GREEN + f"│ {' ':<76}{Fore.GREEN}│")
        
        print(Fore.GREEN + "└─────────────────────────────────────────────────────────────────────────┘" + Style.RESET_ALL)
        
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
            response = "AVAILABLE COMMANDS: camera on, camera off, camera standby, status, help, api test, os info, list files, screen capture, screen start, screen stop, system info, exec [command], launch [app], find [app], running apps, kill [app], memory show, memory clear, shutdown, restart"
        elif cmd == "status":
            cpu = psutil.cpu_percent()
            mem = psutil.virtual_memory().percent
            response = f"SYSTEM STATUS: CPU {cpu}%, RAM {mem}%, CAMERA {self.camera_status}"
        elif cmd == "camera on":
            self.camera_status = "ACTIVE"
            response = self.activate_camera()
        elif cmd == "camera off":
            self.camera_status = "OFF"
            response = self.deactivate_camera()
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
        elif cmd == "screen capture":
            if screen_monitor_available:
                screenshot_path = screen_monitor.capture_screen()
                if screenshot_path:
                    response = f"SCREEN CAPTURED: {screenshot_path}"
                else:
                    response = "SCREEN CAPTURE FAILED."
            else:
                response = "SCREEN MONITOR NOT AVAILABLE."
        elif cmd == "screen start":
            if screen_monitor_available:
                response = screen_monitor.start_monitoring()
            else:
                response = "SCREEN MONITOR NOT AVAILABLE."
        elif cmd == "screen stop":
            if screen_monitor_available:
                response = screen_monitor.stop_monitoring()
            else:
                response = "SCREEN MONITOR NOT AVAILABLE."
        elif cmd == "system info":
            if screen_monitor_available:
                sys_info = screen_monitor.get_system_info()
                response = f"SYSTEM INFO: {sys_info['platform']} | CPU: {sys_info['cpu_percent']}% | RAM: {sys_info['memory_percent']}%"
            else:
                response = "SCREEN MONITOR NOT AVAILABLE."
        elif cmd.startswith("exec "):
            if screen_monitor_available:
                command_to_run = cmd[5:]  # Remove "exec " from the command
                result = screen_monitor.execute_command(command_to_run)
                if result['success']:
                    response = f"COMMAND OUTPUT: {result['stdout'][:200]}..."  # Limit output length
                else:
                    response = f"COMMAND ERROR: {result['error']}"
            else:
                response = "SCREEN MONITOR NOT AVAILABLE."
        elif cmd.startswith("launch "):
            if app_launcher_available:
                app_name = cmd[7:]  # Remove "launch " from the command
                result = app_launcher.launch_by_name(app_name)
                if result['success']:
                    response = f"APPLICATION LAUNCHED: {result['message']}"
                else:
                    response = f"LAUNCH ERROR: {result['error']}"
            else:
                response = "APP LAUNCHER NOT AVAILABLE."
        elif cmd.startswith("find "):
            if app_launcher_available:
                app_name = cmd[5:]  # Remove "find " from the command
                app_path = app_launcher.find_application(app_name)
                if app_path:
                    response = f"APPLICATION FOUND: {app_path}"
                else:
                    response = f"APPLICATION '{app_name}' NOT FOUND."
            else:
                response = "APP LAUNCHER NOT AVAILABLE."
        elif cmd == "running apps":
            if app_launcher_available:
                apps = app_launcher.get_running_apps()
                if isinstance(apps, list):
                    app_names = [app.get('name', 'Unknown') for app in apps[:10]]  # Show first 10
                    response = f"RUNNING APPS: {', '.join(app_names)}"
                else:
                    response = f"ERROR GETTING RUNNING APPS: {apps.get('error', 'Unknown error')}"
            else:
                response = "APP LAUNCHER NOT AVAILABLE."
        elif cmd.startswith("kill "):
            if app_launcher_available:
                app_name = cmd[5:]  # Remove "kill " from the command
                result = app_launcher.kill_application(app_name)
                if result['success']:
                    response = f"APP TERMINATED: {result['message']}"
                else:
                    response = f"KILL ERROR: {result['error']}"
            else:
                response = "APP LAUNCHER NOT AVAILABLE."
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
    
    def activate_camera(self):
        """Activate the camera system"""
        try:
            import cv2
            # Try to access the camera
            cap = cv2.VideoCapture(0)
            if cap.isOpened():
                ret, frame = cap.read()
                if ret:
                    cap.release()
                    return "CAMERA SUBSYSTEM ACTIVATED. LIVE FEED ACTIVE."
                else:
                    cap.release()
                    return "CAMERA SUBSYSTEM ACTIVATED. FEED READY."
            else:
                return "CAMERA SUBSYSTEM ACTIVATED. FEED READY."
        except ImportError:
            return "CAMERA SUBSYSTEM ACTIVATED. CV2 NOT INSTALLED."
        except Exception as e:
            return f"CAMERA SUBSYSTEM ACTIVATED. FEED ERROR: {str(e)}"
    
    def deactivate_camera(self):
        """Deactivate the camera system"""
        try:
            import cv2
            # Close any open camera connections
            cv2.destroyAllWindows()
            return "CAMERA SUBSYSTEM DEACTIVATED."
        except ImportError:
            return "CAMERA SUBSYSTEM DEACTIVATED. CV2 NOT INSTALLED."
        except Exception as e:
            return f"CAMERA SUBSYSTEM DEACTIVATED. ERROR: {str(e)}"
    
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