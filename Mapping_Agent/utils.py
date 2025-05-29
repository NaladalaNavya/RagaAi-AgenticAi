import os
from dotenv import load_dotenv
from google.generativeai import configure

def setup_gemini():
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("❌ GEMINI_API_KEY not found in .env.")
    configure(api_key=api_key)
