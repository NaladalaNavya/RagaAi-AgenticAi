import json

def save_to_json(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def save_llm_output(text, filename):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)
