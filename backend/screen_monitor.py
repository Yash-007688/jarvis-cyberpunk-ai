"""
Screen Monitoring and Computer Access Module
Provides screen capture functionality and computer access capabilities
Integrated with JARVIS API for enhanced functionality
"""

import os
import sys
import time
import json
import requests
import platform
import subprocess
from datetime import datetime
from threading import Thread, Event

try:
    import cv2
    import numpy as np
    from PIL import ImageGrab
    screen_capture_available = True
except ImportError:
    screen_capture_available = False
    print("Warning: Screen capture libraries not installed. Install with: pip install opencv-python pillow numpy")

try:
    import win32api
    import win32con
    import win32gui
    windows_api_available = True
except ImportError:
    windows_api_available = False
    print("Warning: Windows API libraries not installed. Install with: pip install pywin32")


class ScreenMonitor:
    def __init__(self):
        self.is_monitoring = False
        self.monitoring_thread = None
        self.stop_event = Event()
        self.capture_interval = 5  # seconds
        self.screenshots_dir = os.path.join(os.path.dirname(__file__), 'screenshots')
        
        # Create screenshots directory if it doesn't exist
        if not os.path.exists(self.screenshots_dir):
            os.makedirs(self.screenshots_dir)
    
    def capture_screen(self):
        """Capture current screen"""
        if screen_capture_available:
            try:
                # Capture screen using PIL
                screenshot = ImageGrab.grab()
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"screenshot_{timestamp}.png"
                filepath = os.path.join(self.screenshots_dir, filename)
                
                screenshot.save(filepath)
                return filepath
            except Exception as e:
                print(f"Screen capture error: {e}")
                return None
        else:
            print("Screen capture not available. Libraries not installed.")
            return None
    
    def get_active_window_info(self):
        """Get information about the active window"""
        if windows_api_available:
            try:
                hwnd = win32gui.GetForegroundWindow()
                window_title = win32gui.GetWindowText(hwnd)
                window_class = win32gui.GetClassName(hwnd)
                
                return {
                    "title": window_title,
                    "class": window_class,
                    "handle": hwnd
                }
            except Exception as e:
                print(f"Window info error: {e}")
                return None
        else:
            return {"title": "Unknown", "class": "Unknown", "handle": 0}
    
    def get_system_info(self):
        """Get comprehensive system information"""
        try:
            import psutil
            
            # CPU info
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            
            # Memory info
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_total = memory.total
            memory_available = memory.available
            
            # Disk info
            disk = psutil.disk_usage('/')
            disk_percent = (disk.used / disk.total) * 100
            
            # Network info
            net_io = psutil.net_io_counters()
            
            # Boot time
            boot_time = datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
            
            return {
                "platform": platform.platform(),
                "processor": platform.processor(),
                "machine": platform.machine(),
                "node": platform.node(),
                "cpu_percent": cpu_percent,
                "cpu_count": cpu_count,
                "memory_percent": memory_percent,
                "memory_total": memory_total,
                "memory_available": memory_available,
                "disk_percent": disk_percent,
                "boot_time": boot_time,
                "network": {
                    "bytes_sent": net_io.bytes_sent,
                    "bytes_recv": net_io.bytes_recv
                }
            }
        except Exception as e:
            print(f"System info error: {e}")
            return {
                "platform": platform.platform(),
                "processor": platform.processor(),
                "error": str(e)
            }
    
    def execute_command(self, command):
        """Execute system command"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            return {
                "success": True,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Command timed out"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def list_directory(self, path):
        """List directory contents"""
        try:
            if os.path.exists(path):
                items = os.listdir(path)
                return {
                    "success": True,
                    "path": path,
                    "items": items
                }
            else:
                return {
                    "success": False,
                    "error": f"Path does not exist: {path}"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def start_monitoring(self, interval=5):
        """Start continuous screen monitoring"""
        self.capture_interval = interval
        self.is_monitoring = True
        self.stop_event.clear()
        
        self.monitoring_thread = Thread(target=self._monitor_loop)
        self.monitoring_thread.daemon = True
        self.monitoring_thread.start()
        
        return "Screen monitoring started"
    
    def stop_monitoring(self):
        """Stop screen monitoring"""
        self.is_monitoring = False
        self.stop_event.set()
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=2)
        return "Screen monitoring stopped"
    
    def _monitor_loop(self):
        """Internal monitoring loop"""
        while self.is_monitoring and not self.stop_event.is_set():
            try:
                # Capture screen
                screenshot_path = self.capture_screen()
                
                # Get active window info
                window_info = self.get_active_window_info()
                
                # Prepare monitoring data
                monitoring_data = {
                    "timestamp": datetime.now().isoformat(),
                    "screenshot_path": screenshot_path,
                    "active_window": window_info,
                    "system_info": self.get_system_info()
                }
                
                # Save monitoring data
                data_file = os.path.join(self.screenshots_dir, "monitoring_data.json")
                if os.path.exists(data_file):
                    with open(data_file, 'r') as f:
                        existing_data = json.load(f)
                else:
                    existing_data = []
                
                existing_data.append(monitoring_data)
                
                with open(data_file, 'w') as f:
                    json.dump(existing_data, f, indent=2)
                
                # Wait for next capture
                for _ in range(self.capture_interval):
                    if self.stop_event.is_set():
                        break
                    time.sleep(1)
                    
            except Exception as e:
                print(f"Monitoring error: {e}")
                time.sleep(self.capture_interval)
    
    def get_latest_monitoring_data(self):
        """Get the latest monitoring data"""
        data_file = os.path.join(self.screenshots_dir, "monitoring_data.json")
        if os.path.exists(data_file):
            try:
                with open(data_file, 'r') as f:
                    data = json.load(f)
                return data[-1] if data else None
            except Exception as e:
                print(f"Error reading monitoring data: {e}")
                return None
        return None


def main():
    """Main function for testing"""
    monitor = ScreenMonitor()
    
    print("Screen Monitor Module")
    print("=" * 30)
    
    # Test basic functionality
    print("1. Capturing screen...")
    screenshot = monitor.capture_screen()
    if screenshot:
        print(f"   Screenshot saved to: {screenshot}")
    else:
        print("   Screen capture not available")
    
    print("\n2. Getting active window info...")
    window_info = monitor.get_active_window_info()
    print(f"   Active window: {window_info}")
    
    print("\n3. Getting system info...")
    system_info = monitor.get_system_info()
    print(f"   System: {system_info['platform']}")
    
    print("\n4. Testing command execution...")
    result = monitor.execute_command("echo Hello from Screen Monitor!")
    print(f"   Command result: {result['stdout'].strip()}")


if __name__ == "__main__":
    main()