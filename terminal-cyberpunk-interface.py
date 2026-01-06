#!/usr/bin/env python3
"""
Cyberpunk Terminal Interface
A futuristic terminal-based UI with cyberpunk aesthetics
"""

import time
import random
import psutil
import os
import sys
from datetime import datetime
import threading

try:
    from rich.console import Console
    from rich.text import Text
    from rich.panel import Panel
    from rich.box import ROUNDED
    from rich import print
    import colorama
    from colorama import Fore, Back, Style
except ImportError:
    print("Please install required packages: pip install rich colorama psutil")
    sys.exit(1)

# Initialize colorama
colorama.init()

class CyberpunkTerminal:
    def __init__(self):
        self.console = Console()
        self.running = True
        self.ai_responses = [
            "System initialized. Ready for commands.",
            "Cyberpunk AI core online.",
            "Security protocols active.",
            "Scanning network for anomalies...",
            "All systems operational.",
            "Welcome to the cyberpunk future.",
            "Data streams flowing normally.",
            "Firewall status: Maximum security.",
            "Processing request...",
            "Analyzing data patterns..."
        ]
        
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def matrix_rain_effect(self, duration=2):
        """Create a Matrix-style rain effect in the background"""
        chars = "01"
        width, height = os.get_terminal_size()
        
        for _ in range(duration * 10):  # Run for specified duration
            line = ""
            for _ in range(width):
                line += random.choice(chars)
            print(Fore.GREEN + line + Style.RESET_ALL)
            time.sleep(0.05)
            self.clear_screen()
    
    def boot_sequence(self):
        """Simulate a cyberpunk boot sequence"""
        self.clear_screen()
        print(Fore.CYAN + Style.BRIGHT + "=" * 60)
        print(Fore.MAGENTA + Style.BRIGHT + "CYBERPUNK AI TERMINAL v2.0")
        print(Fore.CYAN + Style.BRIGHT + "=" * 60 + Style.RESET_ALL)
        
        boot_messages = [
            "Initializing cyberpunk systems...",
            "Loading neural networks...",
            "Activating security protocols...",
            "Calibrating data streams...",
            "AI core booting...",
            "Neural interface online...",
            "System ready for commands."
        ]
        
        for i, msg in enumerate(boot_messages):
            time.sleep(0.5)
            progress = "=" * (i + 1) + " " * (len(boot_messages) - i - 1)
            print(Fore.CYAN + f"[{progress}] {msg}" + Style.RESET_ALL)
        
        time.sleep(1)
        print(Fore.GREEN + "\n[System] Boot sequence complete!" + Style.RESET_ALL)
        time.sleep(1)
    
    def get_system_stats(self):
        """Get current system statistics"""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        network = psutil.net_io_counters()
        
        return {
            'cpu': cpu_percent,
            'memory': memory.percent,
            'disk': (disk.used / disk.total) * 100,
            'network_sent': network.bytes_sent,
            'network_recv': network.bytes_recv
        }
    
    def draw_hud(self):
        """Draw the main HUD interface"""
        stats = self.get_system_stats()
        
        # Draw header
        print(Fore.CYAN + Style.BRIGHT + "=" * 80)
        print(Fore.MAGENTA + Style.BRIGHT + "CYBERPUNK AI TERMINAL | NEURAL INTERFACE v2.0")
        print(Fore.CYAN + Style.BRIGHT + "=" * 80 + Style.RESET_ALL)
        
        # Draw AI CORE STATUS panel
        print(Fore.GREEN + "┌─ AI CORE STATUS ──────────────────────────────────────────────────────────────┐")
        print(Fore.GREEN + f"│ Status: {Fore.CYAN}ONLINE" + " " * 60 + Fore.GREEN + "│")
        print(Fore.GREEN + f"│ Processing: {Fore.CYAN}ACTIVE" + " " * 57 + Fore.GREEN + "│")
        print(Fore.GREEN + f"│ Neural Pathways: {Fore.CYAN}OPTIMAL" + " " * 52 + Fore.GREEN + "│")
        print(Fore.GREEN + "└─────────────────────────────────────────────────────────────────────────────┘" + Style.RESET_ALL)
        
        # Draw SECURITY FIREWALL panel
        print(Fore.MAGENTA + "┌─ SECURITY FIREWALL ───────────────────────────────────────────────────────────┐")
        print(Fore.MAGENTA + f"│ Firewall: {Fore.CYAN}ACTIVE" + " " * 59 + Fore.MAGENTA + "│")
        print(Fore.MAGENTA + f"│ Threat Level: {Fore.CYAN}LOW" + " " * 57 + Fore.MAGENTA + "│")
        print(Fore.MAGENTA + f"│ Anomalies Detected: {Fore.CYAN}0" + " " * 53 + Fore.MAGENTA + "│")
        print(Fore.MAGENTA + "└─────────────────────────────────────────────────────────────────────────────┘" + Style.RESET_ALL)
        
        # Draw DATA STREAM panel
        print(Fore.CYAN + "┌─ DATA STREAM ─────────────────────────────────────────────────────────────────┐")
        print(Fore.CYAN + f"│ Network In: {Fore.GREEN}{stats['network_recv'] // 1024}KB" + " " * 55 + Fore.CYAN + "│")
        print(Fore.CYAN + f"│ Network Out: {Fore.GREEN}{stats['network_sent'] // 1024}KB" + " " * 54 + Fore.CYAN + "│")
        print(Fore.CYAN + f"│ Active Connections: {Fore.GREEN}{len(psutil.net_connections())}" + " " * 49 + Fore.CYAN + "│")
        print(Fore.CYAN + "└─────────────────────────────────────────────────────────────────────────────┘" + Style.RESET_ALL)
        
        # Draw SYSTEM STATS panel
        print(Fore.GREEN + "┌─ SYSTEM STATS ───────────────────────────────────────────────────────────────┐")
        print(Fore.GREEN + f"│ CPU: {Fore.CYAN}{stats['cpu']:.1f}%" + " " * 10 + f"{'█' * int(stats['cpu'] / 5)}" + " " * (20 - int(stats['cpu'] / 5)) + Fore.GREEN + "│")
        print(Fore.GREEN + f"│ RAM: {Fore.CYAN}{stats['memory']:.1f}%" + " " * 10 + f"{'█' * int(stats['memory'] / 5)}" + " " * (20 - int(stats['memory'] / 5)) + Fore.GREEN + "│")
        print(Fore.GREEN + f"│ DISK: {Fore.CYAN}{stats['disk']:.1f}%" + " " * 9 + f"{'█' * int(stats['disk'] / 5)}" + " " * (20 - int(stats['disk'] / 5)) + Fore.GREEN + "│")
        print(Fore.GREEN + "└─────────────────────────────────────────────────────────────────────────────┘" + Style.RESET_ALL)
        
        # Draw COMMAND MODULE
        print(Fore.MAGENTA + "┌─ COMMAND MODULE ────────────────────────────────────────────────────────────┐")
        print(Fore.MAGENTA + "│ Enter command: " + " " * 59 + Fore.MAGENTA + "│")
        print(Fore.MAGENTA + "└─────────────────────────────────────────────────────────────────────────────┘" + Style.RESET_ALL)
    
    def type_text(self, text, delay=0.03):
        """Simulate typing effect for AI responses"""
        for char in text:
            print(Fore.CYAN + char, end='', flush=True)
            time.sleep(delay)
        print(Style.RESET_ALL)
    
    def display_ai_response(self, response):
        """Display AI response with typing effect"""
        print(Fore.GREEN + "[AI CORE] " + Style.RESET_ALL, end='')
        self.type_text(response)
    
    def run_interface(self):
        """Main interface loop"""
        self.boot_sequence()
        
        while self.running:
            try:
                self.clear_screen()
                self.draw_hud()
                
                # Show current time
                current_time = datetime.now().strftime("%H:%M:%S")
                print(Fore.CYAN + f"\n[SYSTEM TIME: {current_time}] " + Style.RESET_ALL, end='')
                
                # Get user input
                user_input = input(Fore.MAGENTA + "└─> " + Style.RESET_ALL)
                
                if user_input.lower() in ['exit', 'quit', 'q']:
                    print(Fore.RED + "[SYSTEM] Shutting down..." + Style.RESET_ALL)
                    break
                
                # Process command and show response
                if user_input.strip():
                    response = random.choice(self.ai_responses)
                    self.display_ai_response(response)
                    time.sleep(2)  # Pause before next iteration
                
            except KeyboardInterrupt:
                print(Fore.RED + "\n[System] Interrupted. Shutting down..." + Style.RESET_ALL)
                break
            except Exception as e:
                print(Fore.RED + f"[ERROR] {str(e)}" + Style.RESET_ALL)
                time.sleep(2)

def main():
    """Main function to run the cyberpunk terminal"""
    terminal = CyberpunkTerminal()
    terminal.run_interface()

if __name__ == "__main__":
    main()