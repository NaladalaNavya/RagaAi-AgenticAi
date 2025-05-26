import os
from dotenv import load_dotenv

def load_api_key():
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("API key not found. Please set GOOGLE_API_KEY in your environment.")
    return api_key
