from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
import sys
import json
import re

# Add parent directory to path to import config if needed
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from system_controller import SystemController
from media_controller import MediaController
from spotify_controller import SpotifyController

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Configuration
API_KEY = os.getenv("OPENROUTER_API_KEY", "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")
MODEL = os.getenv("MODEL_NAME", "openrouter/auto")

# Initialize Controllers
system_controller = SystemController()
media_controller = MediaController()
spotify_controller = SpotifyController()

# Determine which music controller to use
use_spotify_api = spotify_controller.is_available()
print(f"Music Control: {'Spotify API' if use_spotify_api else 'Media Keys'}")

SYSTEM_PROMPT = """You are JARVIS, an advanced AI assistant with system control and music control capabilities.

You can perform file operations, system commands, and control music playback. When a user asks you to perform an operation, respond with a JSON object in this exact format:

{
  "action": "read_file|write_file|delete_file|rename_file|move_file|copy_file|list_directory|create_directory|delete_directory|execute_command|music_play|music_pause|music_next|music_previous|music_search|music_play_song|music_current|music_volume",
  "params": {
    "file_path": "path/to/file",
    "content": "file content (for write operations)",
    "new_path": "new/path (for rename/move)",
    "destination": "dest/path (for move/copy)",
    "dir_path": "path/to/directory",
    "command": "system command to execute",
    "query": "search query for music",
    "volume": "volume level 0-100"
  },
  "response": "A friendly confirmation message to the user in their language (Hindi/English)"
}

Language Policy:
- Respond in the SAME LANGUAGE as the user (English or Hindi).
- Use Devanagari script for Hindi responses.
- Always keep the JSON keys (action, params, etc.) in English.

Path Guidelines:
- If the user mentions "Desktop", use "Desktop/filename.ext".
- If the user mentions "Documents", use "Documents/filename.ext".
- The system will automatically resolve these to the correct Windows user folders.
- Example: "Create yash.py on desktop" -> {"action": "write_file", "params": {"file_path": "Desktop/yash.py", "content": "..."}, "response": "Creating yash.py on your Desktop."}

File Operation Examples:
- "Read the file test.txt" → {"action": "read_file", "params": {"file_path": "test.txt"}, "response": "Reading test.txt for you now."}
- "test.txt फ़ाइल पढ़ो" → {"action": "read_file", "params": {"file_path": "test.txt"}, "response": "मैं आपके लिए test.txt फ़ाइल पढ़ रहा हूँ।"}

Music Control Examples:
- "Play music" → {"action": "music_play", "params": {}, "response": "Resuming playback."}
- "गाना बजाओ" → {"action": "music_play", "params": {}, "response": "गाना शुरू कर रहा हूँ।"}

If the user is just chatting (not requesting an operation), respond normally in their language without JSON.

Be helpful, precise, and have a slightly robotic but friendly personality (Hindi: विनम्र और पेशेवर रूप)."""

def call_ai(user_input, context_messages=None):
    """Call the AI API"""
    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        if context_messages:
            messages.extend(context_messages)
        messages.append({"role": "user", "content": user_input})
        
        payload = {
            "model": MODEL,
            "messages": messages
        }
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            return None
    except Exception as e:
        print(f"AI Error: {str(e)}")
        return None

def parse_ai_response(ai_response):
    """Parse AI response to extract system commands"""
    try:
        # Try to find JSON in the response
        json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
        if json_match:
            json_str = json_match.group()
            print(f"DEBUG: Found JSON: {json_str}")
            command_data = json.loads(json_str)
            if 'action' in command_data:
                return command_data
        return None
    except Exception as e:
        print(f"DEBUG: JSON Parse Error: {e}")
        return None

def execute_system_command(command_data):
    """Execute a system command based on parsed data"""
    action = command_data.get('action')
    params = command_data.get('params', {})
    
    print(f"DEBUG: Executing action: {action} with params: {params}")
    
    try:
        # File operations
        if action == 'read_file':
            return system_controller.read_file(params.get('file_path', ''))
        elif action == 'write_file':
            return system_controller.write_file(
                params.get('file_path', ''),
                params.get('content', '')
            )
        elif action == 'delete_file':
            return system_controller.delete_file(params.get('file_path', ''))
        elif action == 'rename_file':
            return system_controller.rename_file(
                params.get('file_path', ''),
                params.get('new_path', '')
            )
        elif action == 'move_file':
            return system_controller.move_file(
                params.get('file_path', ''),
                params.get('destination', '')
            )
        elif action == 'copy_file':
            return system_controller.copy_file(
                params.get('file_path', ''),
                params.get('destination', '')
            )
        elif action == 'list_directory':
            return system_controller.list_directory(params.get('dir_path', ''))
        elif action == 'create_directory':
            return system_controller.create_directory(params.get('dir_path', ''))
        elif action == 'delete_directory':
            return system_controller.delete_directory(params.get('dir_path', ''))
        elif action == 'execute_command':
            return system_controller.execute_command(params.get('command', ''))
        
        # Music operations
        elif action == 'music_play':
            return spotify_controller.play() if use_spotify_api else media_controller.play_pause()
        elif action == 'music_pause':
            return spotify_controller.pause() if use_spotify_api else media_controller.play_pause()
        elif action == 'music_next':
            return spotify_controller.next_track() if use_spotify_api else media_controller.next_track()
        elif action == 'music_previous':
            return spotify_controller.previous_track() if use_spotify_api else media_controller.previous_track()
        elif action == 'music_search':
            return spotify_controller.search_track(params.get('query', '')) if use_spotify_api else {"success": False, "error": "Search requires Spotify API"}
        elif action == 'music_play_song':
            return spotify_controller.play_search_result(params.get('query', '')) if use_spotify_api else {"success": False, "error": "Song selection requires Spotify API"}
        elif action == 'music_current':
            return spotify_controller.get_current_playback() if use_spotify_api else {"success": False, "error": "Current track info requires Spotify API"}
        elif action == 'music_volume':
            try:
                volume = int(params.get('volume', 50))
                return spotify_controller.set_volume(volume) if use_spotify_api else media_controller.volume_up() if volume > 50 else media_controller.volume_down()
            except:
                return {"success": False, "error": "Invalid volume value"}
        
        else:
            return {"success": False, "error": f"Unknown action: {action}"}
    except Exception as e:
        print(f"DEBUG: Execution Error: {e}")
        return {"success": False, "error": f"Execution error: {str(e)}"}

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "online", "system": "JARVIS API"})

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('message', '')
    
    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    print(f"Received: {user_input}")

    try:
        # Get AI response
        ai_response = call_ai(user_input)
        
        if not ai_response:
            return jsonify({
                "error": "AI connection failed",
                "reply": "I am unable to connect to the neural network at this time."
            }), 500
        
        # Check if AI wants to execute a system command
        command_data = parse_ai_response(ai_response)
        
        if command_data:
            # Execute the system command
            result = execute_system_command(command_data)
            
            # Format response based on result
            if result.get('success'):
                response_text = command_data.get('response', 'Operation completed.')
                
                # Add specific details based on action
                if command_data['action'] == 'read_file' and 'content' in result:
                    response_text += f"\n\nFile contents:\n{result['content']}"
                elif command_data['action'] == 'list_directory' and 'items' in result:
                    items_text = "\n".join([f"- {item['name']} ({item['type']})" for item in result['items'][:20]])
                    response_text += f"\n\nFound {result['count']} items:\n{items_text}"
                    if result['count'] > 20:
                        response_text += f"\n... and {result['count'] - 20} more items"
                elif 'message' in result:
                    response_text += f"\n{result['message']}"
                
                return jsonify({
                    "reply": response_text,
                    "system_result": result,
                    "action": command_data['action']
                })
            else:
                error_msg = result.get('error', 'Unknown error')
                return jsonify({
                    "reply": f"I encountered an error: {error_msg}",
                    "system_result": result,
                    "action": command_data['action']
                })
        else:
            # Regular chat response
            return jsonify({"reply": ai_response})

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({
            "error": str(e),
            "reply": "An internal system error occurred."
        }), 500

@app.route('/system/execute', methods=['POST'])
def system_execute():
    """Direct system command execution endpoint"""
    data = request.json
    action = data.get('action')
    params = data.get('params', {})
    
    if not action:
        return jsonify({"error": "No action specified"}), 400
    
    try:
        result = execute_system_command({"action": action, "params": params})
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    print("Starting JARVIS Backend Server on port 5000...")
    print("System Control: ENABLED")
    app.run(host='0.0.0.0', port=5000)
