"""
Simple script to run the model training process
"""

from model_trainer import ModelTrainer
import os

def main():
    print("Starting AI Agent Brain Training Process...")
    print("="*50)
    
    # Initialize the trainer
    trainer = ModelTrainer()
    
    # Check if API key is set
    if trainer.api_key == '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':
        print("WARNING: OpenRouter API key needs to be updated!")
        print("Please update your OPENROUTER_API_KEY in the config or .env file with your personal API key.")
        print("Copy .env.example to .env and add your API key.")
        return
    
    print(f"Using API key: {trainer.api_key[:8]}..." if len(trainer.api_key) > 8 else "API key configured")
    
    # Load training data
    data_path = os.path.join(trainer.config.TRAINING_DATA_PATH, 'dummy_training_data.json')
    
    # Create dummy training data if it doesn't exist
    if not os.path.exists(data_path):
        dummy_training_data = []
        for i in range(50):  # Create 50 dummy training examples
            dummy_training_data.append({
                'input': f'Dummy training input {i}',
                'output': f'Dummy training output {i} following the speech patterns and tone guidelines',
                'context': 'AI Agent conversation'
            })
        
        # Save dummy data to file
        import json
        os.makedirs(trainer.config.TRAINING_DATA_PATH, exist_ok=True)
        with open(data_path, 'w', encoding='utf-8') as f:
            json.dump(dummy_training_data, f, indent=2)
        print(f"Created dummy training data at {data_path}")
    
    # Load the training data
    trainer.load_training_data(data_path)
    
    # Perform fine-tuning
    print("\nStarting training process...")
    training_history = trainer.fine_tune_model(epochs=trainer.config.TRAINING_EPOCHS)
    
    # Save the trained model
    model_path = trainer.save_model()
    
    # Evaluate the model
    evaluation_results = trainer.evaluate_training_effectiveness()
    
    print("\n" + "="*50)
    print("Training process completed successfully!")
    print(f"Model saved to: {model_path}")
    print("Next steps:")
    print("1. Review the training history and evaluation results")
    print("2. Test the model with real conversation data")
    print("3. Iterate on training data to improve performance")


if __name__ == "__main__":
    main()