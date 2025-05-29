from intake.utils import model, extract_json

def post_analysis_and_followup(patient_data):
    prompt = f\"\"\"You are a medical assistant reviewing the following patient data:
    (same follow-up prompt from your original code)
    \"\"\"

    response = model.start_chat(history=[])
    reply = response.send_message(prompt)
    updated_data = dict(patient_data)

    while True:
        if "```json" in reply.text or "{" in reply.text:
            result = extract_json(reply.text)
            if result.get("status") == "finalized":
                return result.get("updated_patient_data", updated_data), result.get("notes", "")
        
        print(f"\n🤖 {reply.text.strip()}")
        user_input = input("👤 ").strip()
        reply = response.send_message(user_input)
