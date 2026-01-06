import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from typing import Dict, Any, List, Optional

class SpotifyController:
    """Controls Spotify playback using Spotify Web API"""
    
    def __init__(self):
        self.sp = None
        self.authenticated = False
        self._initialize_spotify()
    
    def _initialize_spotify(self):
        """Initialize Spotify client with OAuth"""
        try:
            # Get credentials from environment or use defaults
            client_id = os.getenv('SPOTIFY_CLIENT_ID', '')
            client_secret = os.getenv('SPOTIFY_CLIENT_SECRET', '')
            redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI', 'http://localhost:8888/callback')
            
            if not client_id or not client_secret:
                print("Spotify credentials not found. Using media keys only.")
                return
            
            scope = "user-read-playback-state user-modify-playback-state user-read-currently-playing"
            
            self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                client_id=client_id,
                client_secret=client_secret,
                redirect_uri=redirect_uri,
                scope=scope,
                cache_path=".spotify_cache"
            ))
            
            self.authenticated = True
            print("Spotify API: Authenticated successfully")
            
        except Exception as e:
            print(f"Spotify API initialization failed: {e}")
            self.authenticated = False
    
    def is_available(self) -> bool:
        """Check if Spotify API is available"""
        return self.authenticated and self.sp is not None
    
    def get_current_playback(self) -> Dict[str, Any]:
        """Get current playback information"""
        try:
            if not self.is_available():
                return {"success": False, "error": "Spotify API not available"}
            
            playback = self.sp.current_playback()
            
            if not playback:
                return {
                    "success": True,
                    "is_playing": False,
                    "message": "No active playback"
                }
            
            track = playback.get('item', {})
            
            return {
                "success": True,
                "is_playing": playback.get('is_playing', False),
                "track_name": track.get('name', 'Unknown'),
                "artist": ', '.join([artist['name'] for artist in track.get('artists', [])]),
                "album": track.get('album', {}).get('name', 'Unknown'),
                "album_art": track.get('album', {}).get('images', [{}])[0].get('url', ''),
                "progress_ms": playback.get('progress_ms', 0),
                "duration_ms": track.get('duration_ms', 0),
                "volume": playback.get('device', {}).get('volume_percent', 0)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def play(self) -> Dict[str, Any]:
        """Resume playback"""
        try:
            if not self.is_available():
                return {"success": False, "error": "Spotify API not available"}
            
            self.sp.start_playback()
            return {
                "success": True,
                "message": "Playback resumed",
                "action": "play"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def pause(self) -> Dict[str, Any]:
        """Pause playback"""
        try:
            if not self.is_available():
                return {"success": False, "error": "Spotify API not available"}
            
            self.sp.pause_playback()
            return {
                "success": True,
                "message": "Playback paused",
                "action": "pause"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def next_track(self) -> Dict[str, Any]:
        """Skip to next track"""
        try:
            if not self.is_available():
                return {"success": False, "error": "Spotify API not available"}
            
            self.sp.next_track()
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
            if not self.is_available():
                return {"success": False, "error": "Spotify API not available"}
            
            self.sp.previous_track()
            return {
                "success": True,
                "message": "Went back to previous track",
                "action": "previous"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def search_track(self, query: str, limit: int = 5) -> Dict[str, Any]:
        """Search for tracks"""
        try:
            if not self.is_available():
                return {"success": False, "error": "Spotify API not available"}
            
            results = self.sp.search(q=query, type='track', limit=limit)
            tracks = results.get('tracks', {}).get('items', [])
            
            if not tracks:
                return {
                    "success": True,
                    "tracks": [],
                    "message": f"No tracks found for '{query}'"
                }
            
            track_list = []
            for track in tracks:
                track_list.append({
                    "name": track['name'],
                    "artist": ', '.join([artist['name'] for artist in track['artists']]),
                    "album": track['album']['name'],
                    "uri": track['uri'],
                    "duration_ms": track['duration_ms']
                })
            
            return {
                "success": True,
                "tracks": track_list,
                "count": len(track_list)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def play_track(self, uri: str) -> Dict[str, Any]:
        """Play a specific track by URI"""
        try:
            if not self.is_available():
                return {"success": False, "error": "Spotify API not available"}
            
            self.sp.start_playback(uris=[uri])
            return {
                "success": True,
                "message": "Now playing track",
                "action": "play_track"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def play_search_result(self, query: str) -> Dict[str, Any]:
        """Search for a track and play the first result"""
        try:
            if not self.is_available():
                return {"success": False, "error": "Spotify API not available"}
            
            # Search for the track
            search_result = self.search_track(query, limit=1)
            
            if not search_result.get('success') or not search_result.get('tracks'):
                return {
                    "success": False,
                    "error": f"Could not find '{query}'"
                }
            
            # Play the first result
            track = search_result['tracks'][0]
            play_result = self.play_track(track['uri'])
            
            if play_result.get('success'):
                return {
                    "success": True,
                    "message": f"Now playing {track['name']} by {track['artist']}",
                    "track": track,
                    "action": "play_search"
                }
            else:
                return play_result
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def set_volume(self, volume: int) -> Dict[str, Any]:
        """Set playback volume (0-100)"""
        try:
            if not self.is_available():
                return {"success": False, "error": "Spotify API not available"}
            
            volume = max(0, min(100, volume))  # Clamp between 0-100
            self.sp.volume(volume)
            
            return {
                "success": True,
                "message": f"Volume set to {volume}%",
                "volume": volume,
                "action": "volume"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def add_to_queue(self, uri: str) -> Dict[str, Any]:
        """Add track to queue"""
        try:
            if not self.is_available():
                return {"success": False, "error": "Spotify API not available"}
            
            self.sp.add_to_queue(uri)
            return {
                "success": True,
                "message": "Track added to queue",
                "action": "queue"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def toggle_shuffle(self, state: bool) -> Dict[str, Any]:
        """Toggle shuffle mode"""
        try:
            if not self.is_available():
                return {"success": False, "error": "Spotify API not available"}
            
            self.sp.shuffle(state)
            return {
                "success": True,
                "message": f"Shuffle {'enabled' if state else 'disabled'}",
                "shuffle": state,
                "action": "shuffle"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
