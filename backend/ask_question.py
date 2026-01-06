"""
Script to send a question to the OpenRouter API
"""

import requests
from config import brain_config

def ask_question(question):
    """Send a question to the OpenRouter API and return the response"""
    print(f"Asking: {question}")
    
    # Get API configuration
    api_key = brain_config.OPENROUTER_API_KEY
    model = brain_config.MODEL_NAME
    
    print(f"Using API key: {api_key[:8]}..." if len(api_key) > 8 else "Using API key")
    print(f"Using model: {model}")
    
    # API endpoint
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    # Question request
    data = {
        'model': model,
        'messages': [
            {'role': 'user', 'content': question}
        ],
        'temperature': brain_config.MODEL_TEMPERATURE,
        'max_tokens': brain_config.MODEL_MAX_TOKENS
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
            print(f"✅ Response received!")
            print(f"Answer: {message}")
            return message
        else:
            print(f"❌ API request failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error making API request: {str(e)}")
        return None

if __name__ == "__main__":
    print("Ask a Question to OpenRouter API")
    print("=" * 40)
    
    # Ask the specific question
    question = "what is onedrive"
    answer = ask_question(question)
    
    if answer:
        print("\n🎉 Question answered successfully!")
    else:
        print("\n💥 Failed to get answer from API.")