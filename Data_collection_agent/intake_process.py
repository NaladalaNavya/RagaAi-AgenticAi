import json
from phase1_dynamic_intake import dynamic_medical_intake
from phase2_followup import post_analysis_and_followup
from phase3_specialist import recommend_specialist
from phase4_mandatory_fields import confirm_mandatory_fields

def run_intake_pipeline():
    patient_data, summary = dynamic_medical_intake()
    final_data, notes = post_analysis_and_followup(patient_data)
    specialists, rationale = recommend_specialist(final_data)

    final_output = {
        "summary": summary,
        "patient_data": final_data,
        "followup_notes": notes,
        "recommended_specialist": specialists,
        "specialist_rationale": rationale,
        "status": "complete"
    }

    print("\n✅ Final Output Before Mandatory Check:\n")
    print(json.dumps(final_output, indent=2))

    # Final validation
    enriched_data = confirm_mandatory_fields(final_output)
    final_output["patient_data"] = enriched_data["patient_data"]

    with open("final_patient_summary.json", "w") as f:
        json.dump(final_output, f, indent=2)

    print("\n✅ Final JSON with mandatory fields updated saved.")
