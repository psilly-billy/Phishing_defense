#config_loader.py
import json
import os

def load_credentials(filepath='config/credentials.json'):
    """Load credentials from a JSON file."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Credentials file not found at {filepath}")
    
    with open(filepath, 'r') as f:
        credentials = json.load(f)
        
    gemini_api_key = credentials.get('gemini', {}).get('api_key')
    if not gemini_api_key:
        raise ValueError("Gemini API key not found in credentials file")
    
    return gemini_api_key
