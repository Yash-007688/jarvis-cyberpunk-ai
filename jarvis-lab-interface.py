#!/usr/bin/env python3
"""
JARVIS-Style Lab Interface
A cyberpunk terminal interface with fixed HUD zones
"""

import time
import random
import psutil
import os
import sys
from datetime import datetime
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.box import ROUNDED
from rich import print as rprint
import colorama
from colorama import Fore, Back, Style

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
        
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
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
    
    def draw_camera_hud(self):
        """Draw camera status HUD in top-left"""
        status_colors = {
            "OFF": Fore.RED,
            "STANDBY": Fore.YELLOW,
            "ACTIVE": Fore.GREEN
        }
        
        status_color = status_colors.get(self.camera_status, Fore.RED)
        
        # Create visual indicator animation
        if self.camera_status == "STANDBY":
            indicator = "●" if int(time.time() * 2) % 2 else "○"
        elif self.camera_status == "ACTIVE":
            indicator = "●"
        else:
            indicator = "○"
        
        print(Fore.CYAN + "┌─ CAMERA SUBSYSTEM ──────────────────┐")
        print(Fore.CYAN + f"│ Status: {status_color}{self.camera_status:<15}{' ' * (14-len(self.camera_status))}{Fore.CYAN}│")
        print(Fore.CYAN + f"│ Indicator: {status_color}{indicator}{Fore.CYAN}{' ' * 25}│")
        print(Fore.CYAN + "└────────────────────────────────────┘" + Style.RESET_ALL)
    
    def draw_system_stats(self):
        """Draw system stats in top-right"""
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Calculate bar lengths for visual representation
        cpu_bar = "█" * int(cpu_percent / 5) + "░" * (20 - int(cpu_percent / 5))
        mem_bar = "█" * int(memory.percent / 5) + "░" * (20 - int(memory.percent / 5))
        disk_bar = "█" * int((disk.used / disk.total) * 100 / 5) + "░" * (20 - int((disk.used / disk.total) * 100 / 5))
        
        print(Fore.MAGENTA + "┌─ SYSTEM STATS ────────────────────┐")
        print(Fore.MAGENTA + f"│ CPU: {Fore.CYAN}{cpu_percent:5.1f}%{Fore.MAGENTA}{' ' * (12-len(f'{cpu_percent:.1f}'))}│")
        print(Fore.MAGENTA + f"│ {cpu_bar}{Fore.MAGENTA}│")
        print(Fore.MAGENTA + f"│ RAM: {Fore.CYAN}{memory.percent:5.1f}%{Fore.MAGENTA}{' ' * (12-len(f'{memory.percent:.1f}'))}│")
        print(Fore.MAGENTA + f"│ {mem_bar}{Fore.MAGENTA}│")
        print(Fore.MAGENTA + f"│ DISK:{Fore.CYAN}{(disk.used/disk.total)*100:5.1f}%{Fore.MAGENTA}{' ' * (12-len(f'{(disk.used/disk.total)*100:.1f}'))}│")
        print(Fore.MAGENTA + f"│ {disk_bar}{Fore.MAGENTA}│")
        print(Fore.MAGENTA + f"│ TIME:{Fore.CYAN}{datetime.now().strftime('%H:%M:%S')}{Fore.MAGENTA}{' ' * (11-len(datetime.now().strftime('%H:%M:%S')))}│")
        print(Fore.MAGENTA + "└──────────────────────────────────┘" + Style.RESET_ALL)
    
    def draw_ai_core(self):
        """Draw AI core display in center"""
        # Add some random data to data stream occasionally
        if random.random() < 0.1:  # 10% chance to add new data
            self.data_stream.append(f"[{datetime.now().strftime('%H:%M:%S')}] ANALYZING DATA...")
            if len(self.data_stream) > 10:
                self.data_stream.pop(0)
        
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
    
    def draw_data_stream(self):
        """Draw data stream in bottom-left"""
        print(Fore.CYAN + "┌─ DATA STREAM ──────────────────┐")
        
        # Add matrix-style effect to data stream
        for i in range(6):
            if i < len(self.data_stream):
                line = self.data_stream[i][-28:]  # Show last 28 chars to fit
                print(Fore.CYAN + f"│ {Fore.GREEN}{line:<28}{Fore.CYAN}│")
            else:
                # Generate random matrix-style data
                if random.random() < 0.3:
                    matrix_data = ''.join([random.choice('01') for _ in range(10)])
                    print(Fore.CYAN + f"│ {Fore.GREEN}{matrix_data:<28}{Fore.CYAN}│")
                else:
                    print(Fore.CYAN + f"│ {' ':<28}{Fore.CYAN}│")
        
        print(Fore.CYAN + "└───────────────────────────────┘" + Style.RESET_ALL)
    
    def draw_command_module(self):
        """Draw command module in bottom-right"""
        print(Fore.MAGENTA + "┌─ COMMAND MODULE ──────────────┐")
        print(Fore.MAGENTA + f"│ {' ':<28}{Fore.MAGENTA}│")
        print(Fore.MAGENTA + f"│ {' ':<28}{Fore.MAGENTA}│")
        print(Fore.MAGENTA + f"│ {' ':<28}{Fore.MAGENTA}│")
        print(Fore.MAGENTA + f"│ {' ':<28}{Fore.MAGENTA}│")
        print(Fore.MAGENTA + f"│ {' ':<28}{Fore.MAGENTA}│")
        print(Fore.MAGENTA + "└──────────────────────────────┘" + Style.RESET_ALL)
    
    def type_text(self, text, delay=0.02):
        """Simulate typing effect for AI responses"""
        for char in text:
            print(Fore.CYAN + char, end='', flush=True)
            time.sleep(delay)
        print(Style.RESET_ALL)
    
    def process_command(self, command):
        """Process user commands"""
        cmd = command.lower().strip()
        
        if cmd == "help":
            response = "AVAILABLE COMMANDS: camera on, camera off, camera standby, status, help"
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
        elif cmd == "":
            response = "AWAITING COMMAND INPUT."
        else:
            response = f"UNRECOGNIZED COMMAND: {command}. TYPE 'help' FOR AVAILABLE COMMANDS."
        
        self.ai_response = response
        self.command_history.append(command)
        
        # Add response to data stream
        self.data_stream.append(f"[{datetime.now().strftime('%H:%M:%S')}] {response[:50]}")
        if len(self.data_stream) > 10:
            self.data_stream.pop(0)
    
    def draw_interface(self):
        """Draw the complete interface with fixed zones"""
        # Get system stats
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
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
                right_part = f"│ CPU: {cpu_percent:5.1f}%                     │"
            elif i == 2:
                # Indicator line
                if self.camera_status == "STANDBY":
                    indicator = "●" if int(time.time() * 2) % 2 else "○"
                elif self.camera_status == "ACTIVE":
                    indicator = "●"
                else:
                    indicator = "○"
                left_part = f"│ Indicator: {indicator}                      │"
                right_part = f"│ {'█' * int(cpu_percent / 5) + '░' * (20 - int(cpu_percent / 5)):<20}│"
            elif i == 3:
                # RAM line
                left_part = "│                                   │"
                right_part = f"│ RAM: {memory.percent:5.1f}%                     │"
            elif i == 4:
                # Bottom border
                left_part = "└────────────────────────────────────┘"
                right_part = f"│ {'█' * int(memory.percent / 5) + '░' * (20 - int(memory.percent / 5)):<20}│"
            elif i == 5:
                # Additional line for system stats
                left_part = "                                "
                right_part = f"│ DISK:{(disk.used/disk.total)*100:5.1f}%                     │"
            elif i == 6:
                # Additional line for system stats
                left_part = "                                "
                right_part = f"│ {'█' * int((disk.used/disk.total)*100 / 5) + '░' * (20 - int((disk.used/disk.total)*100 / 5)):<20}│"
            elif i == 7:
                # Additional line for system stats
                left_part = "                                "
                right_part = f"│ TIME:{datetime.now().strftime('%H:%M:%S')}                     │"
            elif i == 8:
                # Bottom border for system stats
                left_part = "                                "
                right_part = "└──────────────────────────────────┘"
            
            # Ensure both panels have same height by filling with empty space if needed
            if i < 5:  # Only print for the main 5-line panels
                print(Fore.CYAN + left_part + Fore.MAGENTA + right_part + Style.RESET_ALL)
        
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