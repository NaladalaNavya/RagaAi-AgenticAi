import os
from dotenv import load_dotenv
from google.generativeai import configure

def load_api_key():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not set in environment")
    configure(api_key=api_key)
