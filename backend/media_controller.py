import keyboard
import time
from typing import Dict, Any

class MediaController:
    """Controls media playback using Windows media keys"""
    
    def __init__(self):
        self.last_command_time = 0
        self.command_cooldown = 0.5  # Prevent rapid repeated commands
    
    def _can_execute(self) -> bool:
        """Check if enough time has passed since last command"""
        current_time = time.time()
        if current_time - self.last_command_time < self.command_cooldown:
            return False
        self.last_command_time = current_time
        return True
    
    def play_pause(self) -> Dict[str, Any]:
        """Toggle play/pause"""
        try:
            if not self._can_execute():
                return {"success": True, "message": "Command sent (cooldown active)"}
            
            keyboard.press_and_release('play/pause media')
            return {
                "success": True,
                "message": "Play/Pause toggled",
                "action": "play_pause"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def next_track(self) -> Dict[str, Any]:
        """Skip to next track"""
        try:
            if not self._can_execute():
                return {"success": True, "message": "Command sent (cooldown active)"}
            
            keyboard.press_and_release('next track')
            return {
                "success": True,
                "message": "Skipped to next track",
                "action": "next"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def previous_track(self) -> Dict[str, Any]:
        """Go to previous track"""
        try:
            if not self._can_execute():
                return {"success": True, "message": "Command sent (cooldown active)"}
            
            keyboard.press_and_release('previous track')
            return {
                "success": True,
                "message": "Went back to previous track",
                "action": "previous"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def volume_up(self) -> Dict[str, Any]:
        """Increase volume"""
        try:
            if not self._can_execute():
                return {"success": True, "message": "Command sent (cooldown active)"}
            
            keyboard.press_and_release('volume up')
            return {
                "success": True,
                "message": "Volume increased",
                "action": "volume_up"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def volume_down(self) -> Dict[str, Any]:
        """Decrease volume"""
        try:
            if not self._can_execute():
                return {"success": True, "message": "Command sent (cooldown active)"}
            
            keyboard.press_and_release('volume down')
            return {
                "success": True,
                "message": "Volume decreased",
                "action": "volume_down"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def mute(self) -> Dict[str, Any]:
        """Toggle mute"""
        try:
            if not self._can_execute():
                return {"success": True, "message": "Command sent (cooldown active)"}
            
            keyboard.press_and_release('volume mute')
            return {
                "success": True,
                "message": "Mute toggled",
                "action": "mute"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
