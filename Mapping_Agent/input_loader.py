import json
import sys

def load_input_json(file_path):
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print("❌ Invalid JSON format.")
        sys.exit(1)
