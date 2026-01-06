"""
Application Launcher Module
Provides functionality to start any application on the computer
Integrated with JARVIS API for enhanced functionality
"""

import os
import sys
import subprocess
import platform
import json
from datetime import datetime
from pathlib import Path


class AppLauncher:
    def __init__(self):
        self.platform = platform.system().lower()
        self.apps_history = []
    
    def find_application(self, app_name):
        """Find application path based on the application name"""
        app_name_lower = app_name.lower()
        
        if self.platform == "windows":
            # Common Windows application locations
            common_paths = [
                r"C:\Program Files",
                r"C:\Program Files (x86)",
                r"C:\Users",
                os.path.expanduser("~\\AppData\\Local\\Microsoft\\WindowsApps"),
                r"C:\Windows",
                r"C:\Windows\System32"
            ]
            
            for path in common_paths:
                if os.path.exists(path):
                    for root, dirs, files in os.walk(path):
                        for file in files:
                            if app_name_lower in file.lower() and (file.lower().endswith('.exe') or file.lower().endswith('.lnk')):
                                return os.path.join(root, file)
        
        elif self.platform == "darwin":  # macOS
            common_paths = [
                "/Applications",
                os.path.expanduser("~/Applications"),
                "/System/Applications",
                "/System/Applications/Utilities"
            ]
            
            for path in common_paths:
                if os.path.exists(path):
                    for item in os.listdir(path):
                        if app_name_lower in item.lower() and item.lower().endswith('.app'):
                            return os.path.join(path, item)
        
        elif self.platform == "linux":
            common_paths = [
                "/usr/bin",
                "/usr/local/bin",
                "/opt",
                os.path.expanduser("~/.local/bin")
            ]
            
            for path in common_paths:
                if os.path.exists(path):
                    for item in os.listdir(path):
                        if app_name_lower in item.lower():
                            return os.path.join(path, item)
        
        return None
    
    def launch_application(self, app_path, args=None):
        """Launch application with optional arguments"""
        try:
            cmd = [app_path]
            if args:
                cmd.extend(args)
            
            # Record launch in history
            launch_record = {
                "timestamp": datetime.now().isoformat(),
                "app_path": app_path,
                "args": args,
                "platform": self.platform
            }
            self.apps_history.append(launch_record)
            
            # Launch the application
            if self.platform == "windows":
                process = subprocess.Popen(
                    cmd,
                    shell=True,
                    creationflags=subprocess.CREATE_NEW_CONSOLE  # Opens in new console window
                )
            else:
                process = subprocess.Popen(cmd)
            
            return {
                "success": True,
                "pid": process.pid,
                "message": f"Application launched successfully with PID {process.pid}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def launch_by_name(self, app_name, args=None):
        """Launch application by name (finds the application first)"""
        app_path = self.find_application(app_name)
        if app_path:
            return self.launch_application(app_path, args)
        else:
            return {
                "success": False,
                "error": f"Application '{app_name}' not found on the system"
            }
    
    def get_running_apps(self):
        """Get list of currently running applications"""
        try:
            if self.platform == "windows":
                result = subprocess.run(
                    ["tasklist", "/fo", "csv"],
                    capture_output=True,
                    text=True
                )
                lines = result.stdout.strip().split('\n')[1:]  # Skip header
                apps = []
                for line in lines:
                    if line:
                        parts = line.strip('"').split('","')
                        if len(parts) >= 2:
                            apps.append({
                                "name": parts[0].strip('"'),
                                "pid": parts[1].strip('"'),
                                "memory": parts[4] if len(parts) > 4 else "N/A"
                            })
                return apps
            elif self.platform == "darwin":
                result = subprocess.run(
                    ["ps", "-eo", "pid,comm"],
                    capture_output=True,
                    text=True
                )
                lines = result.stdout.strip().split('\n')[1:]
                apps = []
                for line in lines:
                    if line.strip():
                        parts = line.strip().split(maxsplit=1)
                        if len(parts) >= 2:
                            apps.append({
                                "name": parts[1],
                                "pid": parts[0]
                            })
                return apps
            else:  # Linux
                result = subprocess.run(
                    ["ps", "-eo", "pid,comm"],
                    capture_output=True,
                    text=True
                )
                lines = result.stdout.strip().split('\n')[1:]
                apps = []
                for line in lines:
                    if line.strip():
                        parts = line.strip().split(maxsplit=1)
                        if len(parts) >= 2:
                            apps.append({
                                "name": parts[1],
                                "pid": parts[0]
                            })
                return apps
        except Exception as e:
            return {"error": str(e)}
    
    def kill_application(self, app_name_or_pid):
        """Kill an application by name or PID"""
        try:
            if self.platform == "windows":
                if app_name_or_pid.isdigit():
                    # It's a PID
                    result = subprocess.run(
                        ["taskkill", "/F", "/PID", app_name_or_pid],
                        capture_output=True,
                        text=True
                    )
                else:
                    # It's an app name
                    result = subprocess.run(
                        ["taskkill", "/F", "/IM", app_name_or_pid],
                        capture_output=True,
                        text=True
                    )
            else:
                if app_name_or_pid.isdigit():
                    # It's a PID
                    result = subprocess.run(
                        ["kill", "-9", app_name_or_pid],
                        capture_output=True,
                        text=True
                    )
                else:
                    # It's an app name
                    result = subprocess.run(
                        ["pkill", "-f", app_name_or_pid],
                        capture_output=True,
                        text=True
                    )
            
            if result.returncode == 0:
                return {"success": True, "message": f"Application '{app_name_or_pid}' terminated"}
            else:
                return {"success": False, "error": result.stderr}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_app_history(self):
        """Get history of launched applications"""
        return self.apps_history
    
    def open_file(self, file_path):
        """Open a file with the default application"""
        try:
            if self.platform == "windows":
                os.startfile(file_path)
            elif self.platform == "darwin":
                subprocess.run(["open", file_path])
            else:  # Linux
                subprocess.run(["xdg-open", file_path])
            
            return {"success": True, "message": f"File opened: {file_path}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def open_url(self, url):
        """Open a URL in the default browser"""
        try:
            if self.platform == "windows":
                os.startfile(url)
            elif self.platform == "darwin":
                subprocess.run(["open", url])
            else:  # Linux
                subprocess.run(["xdg-open", url])
            
            return {"success": True, "message": f"URL opened: {url}"}
        except Exception as e:
            return {"success": False, "error": str(e)}


def main():
    """Main function for testing"""
    launcher = AppLauncher()
    
    print("Application Launcher Module")
    print("=" * 30)
    
    # Test finding and launching applications
    print("Available commands:")
    print("1. find_app <app_name> - Find an application")
    print("2. launch <app_name> - Launch an application by name")
    print("3. launch_path <path> - Launch an application by path")
    print("4. running - Get running applications")
    print("5. kill <app_name_or_pid> - Kill an application")
    print("6. history - Get launch history")
    print("7. open_file <file_path> - Open a file")
    print("8. open_url <url> - Open a URL")
    
    # Example usage
    print(f"\nPlatform: {launcher.platform}")
    
    # Example: Try to find and launch notepad on Windows
    if launcher.platform == "windows":
        result = launcher.launch_by_name("notepad")
        print(f"Launched notepad: {result}")


if __name__ == "__main__":
    main()