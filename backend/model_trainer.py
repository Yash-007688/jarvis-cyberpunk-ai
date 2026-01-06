"""
Model Training Module for AI Agent Brain
Handles training, fine-tuning, and model updates
"""

import json
import os
import pickle
import random
from datetime import datetime
from typing import List, Dict, Any, Optional

try:
    from dotenv import load_dotenv
    load_dotenv()  # Load environment variables from .env file
except ImportError:
    # If python-dotenv is not installed, continue without loading .env file
    pass

import requests

from config import brain_config


class ModelTrainer:
    """
    Class for training and fine-tuning the AI Agent Brain model
    Uses OpenRouter API for training and model updates
    """
    
    def __init__(self):
        self.config = brain_config
        self.api_key = self.config.OPENROUTER_API_KEY
        self.training_data = []
        self.validation_data = []
        
        # Create necessary directories
        os.makedirs(self.config.TRAINING_DATA_PATH, exist_ok=True)
        os.makedirs(self.config.MODEL_SAVE_PATH, exist_ok=True)
    
    def load_training_data(self, data_path: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Load training data from file or directory
        Expected format: List of conversation examples with context and responses
        """
        path = data_path or self.config.TRAINING_DATA_PATH
        
        # Check if it's a single file or directory
        if os.path.isfile(path):
            with open(path, 'r', encoding='utf-8') as f:
                if path.endswith('.json'):
                    self.training_data = json.load(f)
                elif path.endswith('.pkl'):
                    self.training_data = pickle.load(f)
        elif os.path.isdir(path):
            # Look for training data files in the directory
            for filename in os.listdir(path):
                filepath = os.path.join(path, filename)
                if filename.endswith('.json'):
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if isinstance(data, list):
                            self.training_data.extend(data)
        
        # Split data for training and validation (80/20 split)
        random.shuffle(self.training_data)
        split_idx = int(0.8 * len(self.training_data))
        self.validation_data = self.training_data[split_idx:]
        self.training_data = self.training_data[:split_idx]
        
        print(f"Loaded {len(self.training_data)} training examples and {len(self.validation_data)} validation examples")
        return self.training_data
    
    def prepare_training_batch(self, batch_size: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Prepare a batch of training data
        """
        size = batch_size or self.config.TRAINING_BATCH_SIZE
        if len(self.training_data) < size:
            return self.training_data
        return random.sample(self.training_data, size)
    
    def train_step(self, training_batch: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Perform a single training step using OpenRouter API
        Note: Actual model training would typically happen with specialized tools
        This implementation simulates the training process using API calls
        """
        print(f"Performing training step with {len(training_batch)} examples...")
        
        # For demonstration purposes, we'll simulate training metrics
        # In a real implementation, this would involve actual model updates
        metrics = {
            'loss': random.uniform(0.1, 2.0),  # Simulated loss
            'accuracy': random.uniform(0.7, 0.95),  # Simulated accuracy
            'step_time': random.uniform(1.0, 5.0),  # Simulated time in seconds
            'examples_processed': len(training_batch)
        }
        
        # In a real implementation, you would make API calls to train the model
        # This is a placeholder for the actual training logic
        print(f"Training step completed. Metrics: {metrics}")
        
        return metrics
    
    def validate_model(self) -> Dict[str, Any]:
        """
        Validate the model on validation data
        """
        if not self.validation_data:
            print("No validation data available")
            return {}
        
        print(f"Validating on {len(self.validation_data)} examples...")
        
        # Simulate validation metrics
        metrics = {
            'validation_loss': random.uniform(0.1, 2.0),
            'validation_accuracy': random.uniform(0.6, 0.95),
            'examples_processed': len(self.validation_data)
        }
        
        print(f"Validation completed. Metrics: {metrics}")
        return metrics
    
    def fine_tune_model(self, epochs: Optional[int] = None) -> Dict[str, Any]:
        """
        Fine-tune the model using the training data
        """
        epochs = epochs or self.config.TRAINING_EPOCHS
        print(f"Starting fine-tuning for {epochs} epochs...")
        
        training_history = {
            'epoch_losses': [],
            'epoch_accuracies': [],
            'validation_metrics': [],
            'timestamps': []
        }
        
        for epoch in range(epochs):
            print(f"\nEpoch {epoch + 1}/{epochs}")
            
            # Prepare training batch
            training_batch = self.prepare_training_batch()
            
            # Perform training step
            train_metrics = self.train_step(training_batch)
            
            # Validate model
            val_metrics = self.validate_model()
            
            # Record metrics
            training_history['epoch_losses'].append(train_metrics['loss'])
            training_history['epoch_accuracies'].append(train_metrics['accuracy'])
            training_history['validation_metrics'].append(val_metrics)
            training_history['timestamps'].append(datetime.now().isoformat())
            
            print(f"Epoch {epoch + 1} completed. Loss: {train_metrics['loss']:.4f}, "
                  f"Accuracy: {train_metrics['accuracy']:.4f}")
        
        # Save training history
        history_path = os.path.join(self.config.MODEL_SAVE_PATH, f"training_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(history_path, 'w', encoding='utf-8') as f:
            json.dump(training_history, f, indent=2)
        
        print(f"Training completed! History saved to {history_path}")
        return training_history
    
    def save_model(self, model_name: str = None) -> str:
        """
        Save the trained model
        In a real implementation, this would save the actual model weights
        """
        if model_name is None:
            model_name = f"trained_model_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        model_path = os.path.join(self.config.MODEL_SAVE_PATH, f"{model_name}.pkl")
        
        # In a real implementation, you would save the actual model
        # For now, we'll save a placeholder with training config
        model_data = {
            'config': self.config.get_training_config(),
            'timestamp': datetime.now().isoformat(),
            'model_name': model_name
        }
        
        with open(model_path, 'wb') as f:
            pickle.dump(model_data, f)
        
        print(f"Model saved to {model_path}")
        return model_path
    
    def load_model(self, model_path: str) -> Any:
        """
        Load a trained model
        """
        with open(model_path, 'rb') as f:
            model_data = pickle.load(f)
        
        print(f"Model loaded from {model_path}")
        return model_data
    
    def test_model_response(self, prompt: str) -> str:
        """
        Test the model response using OpenRouter API
        """
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': self.config.MODEL_NAME,
            'messages': [
                {'role': 'system', 'content': self.config.SYSTEM_PROMPT},
                {'role': 'user', 'content': prompt}
            ],
            'temperature': self.config.MODEL_TEMPERATURE,
            'max_tokens': self.config.MODEL_MAX_TOKENS
        }
        
        try:
            # Using OpenRouter API endpoint
            response = requests.post(
                'https://openrouter.ai/api/v1/chat/completions',
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                print(f"API request failed with status {response.status_code}: {response.text}")
                return "Error: Failed to get response from model"
        except Exception as e:
            print(f"Error making API request: {str(e)}")
            return f"Error: {str(e)}"
    
    def evaluate_training_effectiveness(self) -> Dict[str, Any]:
        """
        Evaluate how well the training improved the model
        """
        print("Evaluating training effectiveness...")
        
        # Test with a few sample prompts before and after training
        test_prompts = [
            "Hello, how are you?",
            "Can you help me with a technical question?",
            "Tell me about yourself",
            "What are your capabilities?"
        ]
        
        results = {
            'test_prompts': test_prompts,
            'responses': [],
            'timestamp': datetime.now().isoformat()
        }
        
        for prompt in test_prompts:
            response = self.test_model_response(prompt)
            results['responses'].append({
                'prompt': prompt,
                'response': response
            })
        
        # Save evaluation results
        eval_path = os.path.join(self.config.MODEL_SAVE_PATH, f"evaluation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(eval_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        
        print(f"Evaluation completed and saved to {eval_path}")
        return results


def main():
    """
    Main function to demonstrate the training process
    """
    print("AI Agent Brain Model Trainer")
    print("=" * 40)
    
    # Initialize trainer
    trainer = ModelTrainer()
    
    # Load training data (this would typically be pre-existing data)
    # For this example, we'll create some dummy training data
    dummy_training_data = []
    for i in range(50):  # Create 50 dummy training examples
        dummy_training_data.append({
            'input': f'Dummy training input {i}',
            'output': f'Dummy training output {i} following the speech patterns and tone guidelines',
            'context': 'AI Agent conversation'
        })
    
    # Save dummy data to file
    dummy_data_path = os.path.join(trainer.config.TRAINING_DATA_PATH, 'dummy_training_data.json')
    with open(dummy_data_path, 'w', encoding='utf-8') as f:
        json.dump(dummy_training_data, f, indent=2)
    
    print(f"Created dummy training data at {dummy_data_path}")
    
    # Load the training data
    trainer.load_training_data(dummy_data_path)
    
    # Perform fine-tuning
    training_history = trainer.fine_tune_model(epochs=3)  # Use fewer epochs for demo
    
    # Save the trained model
    model_path = trainer.save_model()
    
    # Evaluate the model
    evaluation_results = trainer.evaluate_training_effectiveness()
    
    print("\nTraining process completed!")
    print(f"Model saved to: {model_path}")
    print(f"Training history saved to: {os.path.join(trainer.config.MODEL_SAVE_PATH, 'latest_training_history.json')}")


if __name__ == "__main__":
    main()