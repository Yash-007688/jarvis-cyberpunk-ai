import os
import shutil
import subprocess
import json
from pathlib import Path
from typing import Dict, Any, Optional

class SystemController:
    """Handles all system-level operations for JARVIS"""
    
    def __init__(self):
        self.restricted_paths = [
            'C:\\Windows',
            'C:\\Program Files',
            'C:\\Program Files (x86)',
        ]
    
    def is_safe_path(self, path: str) -> bool:
        """Check if path is safe to operate on"""
        try:
            # Expand ~ to home directory
            path = os.path.expanduser(path)
            abs_path = os.path.abspath(path)
            for restricted in self.restricted_paths:
                if abs_path.lower().startswith(restricted.lower()):
                    return False
            return True
        except:
            return False
    
    def _resolve_path(self, path: str) -> str:
        """Expand common Windows shortcuts and paths"""
        path = os.path.expanduser(path)
        
        # Handle "Desktop", "Documents", etc. if they are at the start
        user_profile = os.environ.get('USERPROFILE', os.path.expanduser('~'))
        
        if path.lower().startswith('desktop/'):
            path = os.path.join(user_profile, 'Desktop', path[8:])
        elif path.lower().startswith('desktop\\'):
            path = os.path.join(user_profile, 'Desktop', path[8:])
        elif path.lower() == 'desktop':
            path = os.path.join(user_profile, 'Desktop')
            
        return path
    
    def read_file(self, file_path: str) -> Dict[str, Any]:
        """Read contents of a file"""
        try:
            file_path = self._resolve_path(file_path)
            if not self.is_safe_path(file_path):
                return {"success": False, "error": "Access to this path is restricted"}
            
            if not os.path.exists(file_path):
                return {"success": False, "error": "File not found"}
            
            if not os.path.isfile(file_path):
                return {"success": False, "error": "Path is not a file"}
            
            # Try to read as text
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                return {
                    "success": True,
                    "content": content,
                    "size": os.path.getsize(file_path),
                    "path": file_path
                }
            except UnicodeDecodeError:
                # Binary file
                return {
                    "success": False,
                    "error": "File is binary and cannot be displayed as text",
                    "size": os.path.getsize(file_path)
                }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def write_file(self, file_path: str, content: str, mode: str = 'w') -> Dict[str, Any]:
        """Write content to a file"""
        try:
            file_path = self._resolve_path(file_path)
            if not self.is_safe_path(file_path):
                return {"success": False, "error": "Access to this path is restricted"}
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
            
            with open(file_path, mode, encoding='utf-8') as f:
                f.write(content)
            
            return {
                "success": True,
                "message": f"File {'created' if mode == 'w' else 'updated'} successfully",
                "path": file_path,
                "size": os.path.getsize(file_path)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def delete_file(self, file_path: str) -> Dict[str, Any]:
        """Delete a file"""
        try:
            file_path = self._resolve_path(file_path)
            if not self.is_safe_path(file_path):
                return {"success": False, "error": "Access to this path is restricted"}
            
            if not os.path.exists(file_path):
                return {"success": False, "error": "File not found"}
            
            if os.path.isfile(file_path):
                os.remove(file_path)
                return {"success": True, "message": f"File deleted: {file_path}"}
            else:
                return {"success": False, "error": "Path is not a file"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def rename_file(self, old_path: str, new_path: str) -> Dict[str, Any]:
        """Rename or move a file"""
        try:
            if not self.is_safe_path(old_path) or not self.is_safe_path(new_path):
                return {"success": False, "error": "Access to this path is restricted"}
            
            if not os.path.exists(old_path):
                return {"success": False, "error": "Source file not found"}
            
            os.rename(old_path, new_path)
            return {
                "success": True,
                "message": f"File renamed from {old_path} to {new_path}",
                "old_path": old_path,
                "new_path": new_path
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def move_file(self, source: str, destination: str) -> Dict[str, Any]:
        """Move a file to a different location"""
        try:
            if not self.is_safe_path(source) or not self.is_safe_path(destination):
                return {"success": False, "error": "Access to this path is restricted"}
            
            if not os.path.exists(source):
                return {"success": False, "error": "Source file not found"}
            
            # If destination is a directory, keep the filename
            if os.path.isdir(destination):
                destination = os.path.join(destination, os.path.basename(source))
            
            shutil.move(source, destination)
            return {
                "success": True,
                "message": f"File moved from {source} to {destination}",
                "source": source,
                "destination": destination
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def copy_file(self, source: str, destination: str) -> Dict[str, Any]:
        """Copy a file to a different location"""
        try:
            if not self.is_safe_path(source) or not self.is_safe_path(destination):
                return {"success": False, "error": "Access to this path is restricted"}
            
            if not os.path.exists(source):
                return {"success": False, "error": "Source file not found"}
            
            # If destination is a directory, keep the filename
            if os.path.isdir(destination):
                destination = os.path.join(destination, os.path.basename(source))
            
            shutil.copy2(source, destination)
            return {
                "success": True,
                "message": f"File copied from {source} to {destination}",
                "source": source,
                "destination": destination
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def list_directory(self, dir_path: str) -> Dict[str, Any]:
        """List contents of a directory"""
        try:
            if not self.is_safe_path(dir_path):
                return {"success": False, "error": "Access to this path is restricted"}
            
            if not os.path.exists(dir_path):
                return {"success": False, "error": "Directory not found"}
            
            if not os.path.isdir(dir_path):
                return {"success": False, "error": "Path is not a directory"}
            
            items = []
            for item in os.listdir(dir_path):
                item_path = os.path.join(dir_path, item)
                is_dir = os.path.isdir(item_path)
                items.append({
                    "name": item,
                    "type": "directory" if is_dir else "file",
                    "size": os.path.getsize(item_path) if not is_dir else None,
                    "path": item_path
                })
            
            return {
                "success": True,
                "path": dir_path,
                "items": items,
                "count": len(items)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def create_directory(self, dir_path: str) -> Dict[str, Any]:
        """Create a new directory"""
        try:
            if not self.is_safe_path(dir_path):
                return {"success": False, "error": "Access to this path is restricted"}
            
            os.makedirs(dir_path, exist_ok=True)
            return {
                "success": True,
                "message": f"Directory created: {dir_path}",
                "path": dir_path
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def delete_directory(self, dir_path: str) -> Dict[str, Any]:
        """Delete a directory"""
        try:
            if not self.is_safe_path(dir_path):
                return {"success": False, "error": "Access to this path is restricted"}
            
            if not os.path.exists(dir_path):
                return {"success": False, "error": "Directory not found"}
            
            if not os.path.isdir(dir_path):
                return {"success": False, "error": "Path is not a directory"}
            
            shutil.rmtree(dir_path)
            return {
                "success": True,
                "message": f"Directory deleted: {dir_path}"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def execute_command(self, command: str, timeout: int = 30) -> Dict[str, Any]:
        """Execute a system command"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr,
                "return_code": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Command execution timed out"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_file_info(self, file_path: str) -> Dict[str, Any]:
        """Get information about a file"""
        try:
            if not self.is_safe_path(file_path):
                return {"success": False, "error": "Access to this path is restricted"}
            
            if not os.path.exists(file_path):
                return {"success": False, "error": "File not found"}
            
            stat = os.stat(file_path)
            return {
                "success": True,
                "path": file_path,
                "size": stat.st_size,
                "created": stat.st_ctime,
                "modified": stat.st_mtime,
                "is_file": os.path.isfile(file_path),
                "is_directory": os.path.isdir(file_path)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
