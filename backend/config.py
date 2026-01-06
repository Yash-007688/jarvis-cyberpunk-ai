"""
Configuration file for the AI Agent Brain
Contains API keys and model configuration
"""

import os
from typing import Dict, Any
try:
    from dotenv import load_dotenv
    load_dotenv()  # Load environment variables from .env file
except ImportError:
    # If python-dotenv is not installed, continue without loading .env file
    pass

class BrainConfig:
    """
    Configuration class for the AI Agent Brain
    Stores API keys, model settings, and training parameters
    """
    
    def __init__(self):
        # OpenRouter API Configuration
        self.OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY', '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')
        
        # Model Configuration
        self.MODEL_NAME = os.getenv('MODEL_NAME', 'openrouter/auto')  # Auto-select best model, change if you want a specific one
        self.MODEL_TEMPERATURE = float(os.getenv('MODEL_TEMPERATURE', '0.7'))
        self.MODEL_MAX_TOKENS = int(os.getenv('MODEL_MAX_TOKENS', '2048'))
        self.MODEL_TOP_P = float(os.getenv('MODEL_TOP_P', '0.9'))
        
        # System Prompt Configuration
        self.SYSTEM_PROMPT = """You are Emenas, an advanced AI assistant with a professional yet approachable tone. 
        You follow the speech patterns and conversation flow guidelines defined in the speech system. 
        Maintain consistency with the established personality and communication style."""
        
        # Training Configuration
        self.TRAINING_DATA_PATH = os.getenv('TRAINING_DATA_PATH', './training_data')
        self.MODEL_SAVE_PATH = os.getenv('MODEL_SAVE_PATH', './trained_models')
        self.TRAINING_EPOCHS = int(os.getenv('TRAINING_EPOCHS', '10'))
        self.TRAINING_BATCH_SIZE = int(os.getenv('TRAINING_BATCH_SIZE', '8'))
        self.TRAINING_LEARNING_RATE = float(os.getenv('TRAINING_LEARNING_RATE', '0.001'))
        
        # Conversation Memory Settings
        self.CONTEXT_WINDOW_SIZE = int(os.getenv('CONTEXT_WINDOW_SIZE', '2048'))
        self.MAX_HISTORY_LENGTH = int(os.getenv('MAX_HISTORY_LENGTH', '50'))
        
        # Voice and Speech Settings
        self.VOICE_RATE = int(os.getenv('VOICE_RATE', '180'))  # Words per minute
        self.VOICE_VOLUME = float(os.getenv('VOICE_VOLUME', '0.9'))  # 0.0 to 1.0
        self.VOICE_TYPE = os.getenv('VOICE_TYPE', 'default')  # 'male', 'female', 'default'
    
    def get_api_config(self) -> Dict[str, Any]:
        """Return API-specific configuration"""
        return {
            'api_key': self.OPENROUTER_API_KEY,
            'model': self.MODEL_NAME,
            'temperature': self.MODEL_TEMPERATURE,
            'max_tokens': self.MODEL_MAX_TOKENS,
            'top_p': self.MODEL_TOP_P
        }
    
    def get_training_config(self) -> Dict[str, Any]:
        """Return training-specific configuration"""
        return {
            'data_path': self.TRAINING_DATA_PATH,
            'save_path': self.MODEL_SAVE_PATH,
            'epochs': self.TRAINING_EPOCHS,
            'batch_size': self.TRAINING_BATCH_SIZE,
            'learning_rate': self.TRAINING_LEARNING_RATE
        }

# Create a global instance of the config
brain_config = BrainConfig()

# Convenience functions to access config values
def get_openrouter_api_key():
    return brain_config.OPENROUTER_API_KEY

def get_model_config():
    return {
        'model': brain_config.MODEL_NAME,
        'temperature': brain_config.MODEL_TEMPERATURE,
        'max_tokens': brain_config.MODEL_MAX_TOKENS,
        'top_p': brain_config.MODEL_TOP_P
    }

def get_voice_settings():
    return {
        'rate': brain_config.VOICE_RATE,
        'volume': brain_config.VOICE_VOLUME,
        'type': brain_config.VOICE_TYPE
    }