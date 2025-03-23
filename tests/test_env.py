import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the API key from environment variables
api_key = os.getenv('GOOGLE_API_KEY')

if api_key:
    print(f"API Key Loaded Successfully: {api_key[:5]}...")  # Print first few characters for confirmation
else:
    print("Failed to load API Key")
