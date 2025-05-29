from google.generativeai import GenerativeModel
from prompt_builder import build_prompt

def get_mapped_output(raw_data):
    model = GenerativeModel("gemini-1.5-flash")
    prompt = build_prompt(raw_data)
    response = model.generate_content(prompt)
    content = response.text.strip()

    if content.startswith("```"):
        content = content.split("```")[1].strip()
        if content.startswith("json"):
            content = content[len("json"):].strip()

    return content
