"""
Test script to check if the OpenRouter API is running and responding
"""

import requests
import json
from config import brain_config

def test_api_connection():
    """Test the OpenRouter API connection"""
    print("Testing OpenRouter API connection...")
    
    # Get API configuration
    api_key = brain_config.OPENROUTER_API_KEY
    model = brain_config.MODEL_NAME
    
    print(f"Using API key: {api_key[:8]}..." if len(api_key) > 8 else "Using API key")
    print(f"Using model: {model}")
    
    # Test API endpoint
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    # Simple test request
    data = {
        'model': model,
        'messages': [
            {'role': 'user', 'content': 'Hello, are you working? Just respond with "API is working".'}
        ]
    }
    
    try:
        print("Sending request to OpenRouter API...")
        response = requests.post(
            'https://openrouter.ai/api/v1/chat/completions',
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            result = response.json()
            message = result['choices'][0]['message']['content']
            print(f"✅ API is working! Response: {message}")
            return True
        else:
            print(f"❌ API request failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error making API request: {str(e)}")
        return False

def test_config_values():
    """Test that configuration values are properly loaded"""
    print("\nTesting configuration values...")
    print(f"API Key loaded: {'Yes' if brain_config.OPENROUTER_API_KEY and brain_config.OPENROUTER_API_KEY != 'your-openrouter-api-key-here' else 'No'}")
    print(f"Model name: {brain_config.MODEL_NAME}")
    print(f"Temperature: {brain_config.MODEL_TEMPERATURE}")
    print(f"Max tokens: {brain_config.MODEL_MAX_TOKENS}")
    print(f"Top P: {brain_config.MODEL_TOP_P}")

if __name__ == "__main__":
    print("OpenRouter API Test")
    print("=" * 30)
    
    # Test configuration
    test_config_values()
    
    # Test API connection
    success = test_api_connection()
    
    if success:
        print("\n🎉 API test completed successfully!")
    else:
        print("\n💥 API test failed. Please check your API key and configuration.")