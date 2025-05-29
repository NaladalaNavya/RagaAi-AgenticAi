from intake import dynamic_medical_intake
from followup import post_analysis_and_followup
from specialist import recommend_specialist
from mandatory_check import confirm_mandatory_fields

def run_pipeline():
    print("=== Step 1: Dynamic Medical Intake ===")
    patient_data, summary = dynamic_medical_intake()

    print("\n=== Step 2: Post-Analysis & Followup ===")
    updated_data, notes = post_analysis_and_followup(patient_data)

    print("\n=== Step 3: Specialist Recommendation ===")
    specialists, rationale = recommend_specialist(updated_data)

    print("\n=== Step 4: Mandatory Fields Confirmation ===")
    final_data = confirm_mandatory_fields({
        "patient_data": updated_data,
        "summary": summary,
        "specialists": specialists,
        "notes": notes
    })

    print("\n\n--- Final Intake Summary ---")
    print(f"Patient Data:\n{final_data['patient_data']}")
    print(f"Recommended Specialists: {final_data.get('specialists', [])}")
    print(f"Summary: {final_data.get('summary', '')}")
    print(f"Additional Notes: {final_data.get('notes', '')}")

if __name__ == "__main__":
    run_pipeline()
