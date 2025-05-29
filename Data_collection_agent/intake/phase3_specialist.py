from intake.utils import model, extract_json
import json

def recommend_specialist(patient_data):
    prompt = f\"\"\"You are a medical triage assistant...
    (trimmed for brevity — same content)
    \"\"\"
    response = model.start_chat(history=[])
    reply = response.send_message(prompt)

    for _ in range(3):
        result = extract_json(reply.text)
        if result.get("status") == "done":
            return result.get("recommended_specialist", []), result.get("rationale", "")
        else:
            break

    print("⚠️ Warning: Specialist recommendation not found.")
    print("LLM response was:\n", reply.text)
    return [], ""
