import sys
import json
from config import load_api_key
from mapper import get_mapped_output

def load_input_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

def main():
    if len(sys.argv) < 2:
        print("❌ Please provide the input JSON file as an argument.")
        print("✅ Example: python main.py final_patient_summary.json")
        return

    input_file = sys.argv[1]
    output_file = "mapped_output.json"

    try:
        raw_data = load_input_json(input_file)
    except FileNotFoundError:
        print(f"❌ File not found: {input_file}")
        return

    try:
        load_api_key()
    except Exception as e:
        print(f"❌ {e}")
        return

    print("🔄 Sending data to Gemini for mapping...")
    mapped_json_str = get_mapped_output(raw_data)

    try:
        mapped_json = json.loads(mapped_json_str)
    except json.JSONDecodeError:
        print("❌ LLM response is not valid JSON. Here's the raw text:")
        print(mapped_json_str)
        return

    with open(output_file, "w") as f:
        json.dump(mapped_json, f, indent=2)

    print(f"✅ Mapped output saved to: {output_file}")

if __name__ == "__main__":
    main()
