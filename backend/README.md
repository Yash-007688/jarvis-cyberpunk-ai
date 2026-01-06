# Backend for AI Agent

This directory contains the backend components for the AI agent, including configuration, model training, and API integration.

## Components

1. **[config.py](file:///c%3A/Users/YASH/Downloads/adism%20ai/backend/config.py)** - Configuration file containing API keys and model settings for the AI brain
2. **[model_trainer.py](file:///c%3A/Users/YASH/Downloads/adism%20ai/backend/model_trainer.py)** - Module for training and fine-tuning the AI agent brain
3. **[train_model.py](file:///c%3A/Users/YASH/Downloads/adism%20ai/backend/train_model.py)** - Simple script to run the training process
4. **[.env.example](file:///c%3A/Users/YASH/Downloads/adism%20ai/backend/.env.example)** - Template for environment variables including API keys

## Configuration

The system uses environment variables for configuration. Copy `.env.example` to `.env` and add your actual API keys:

```bash
cp .env.example .env
```

Then add your OpenRouter API key and other configuration values to the `.env` file.

## Dependencies

Install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

## Training the Model

To run the training process:

```bash
python train_model.py
```

This will load the configuration, create dummy training data if needed, and start the training process.

## API Integration

The backend integrates with OpenRouter API for AI model interactions. The configuration manages API keys and model parameters.