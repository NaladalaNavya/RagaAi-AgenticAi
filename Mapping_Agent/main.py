import sys
from utils import setup_gemini
from input_loader import load_input_json
from gemini_handler import get_mapped_output
from output_writer import save_output

def main():
    if len(sys.argv) < 2:
        print("❌ Please provide the input JSON file.")
        print("✅ Usage: python main.py final_patient_summary.json")
        return

    input_file = sys.argv[1]
    output_file = "mapped_output.json"

    setup_gemini()
    raw_data = load_input_json(input_file)
    print("🔄 Sending data to Gemini for mapping...")
    mapped_json_str = get_mapped_output(raw_data)
    save_output(mapped_json_str, output_file)

if __name__ == "__main__":
    main()
