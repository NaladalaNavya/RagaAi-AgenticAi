import sys
import os
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_injection.intake import collect_patient_data
from data_injection.gemini_formatter import extract_structured_summary
from data_injection.save_data import save_to_json, save_llm_output

def main():
    patient_data = collect_patient_data()
    save_to_json(patient_data, "patient_summary.json")
    print("✅ Patient data saved to 'patient_summary.json'.")

    try:
        summary = extract_structured_summary(patient_data)
        save_llm_output(summary, "patient_summary_llm.json")
        print("✅ LLM summary saved to 'patient_summary_llm.json'.")
    except Exception as e:
        print(f"⚠️ Failed to generate LLM summary: {e}")

if __name__ == "__main__":
    main()
