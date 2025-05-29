import json
from collecting_info import (
    dynamic_medical_intake,
    post_analysis_and_followup,
    recommend_specialist,
    confirm_mandatory_fields,
)

def agent_collect_info(state, config):
    try:
        patient_data, summary = dynamic_medical_intake()
        final_data, notes = post_analysis_and_followup(patient_data)
        specialists, rationale = recommend_specialist(final_data)
        enriched_data = confirm_mandatory_fields({
            "summary": summary,
            "patient_data": final_data,
            "followup_notes": notes,
            "recommended_specialist": specialists,
            "specialist_rationale": rationale,
            "status": "complete"
        })
        print("DEBUG: confirm_mandatory_fields returned:", enriched_data)

        state["patient_data"] = enriched_data["patient_data"]
        state["summary"] = summary
        state["followup_notes"] = notes
        state["recommended_specialist"] = specialists
        state["specialist_rationale"] = rationale

        with open("patient_data.json", "w") as f:
            json.dump(state["patient_data"], f, indent=2)

        return state
    except Exception as e:
        print("Error in agent_collect_info:", e)
        raise
