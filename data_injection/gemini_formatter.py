import google.generativeai as genai
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_injection.config import load_api_key

api_key = load_api_key()
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

def extract_structured_summary(data: dict) -> str:
    prompt = (
        "Format the following patient data into a clean JSON structure for storage:\n\n"
        f"{json.dumps(data, indent=2)}"
    )
    return model.generate_content(prompt).text.strip()
