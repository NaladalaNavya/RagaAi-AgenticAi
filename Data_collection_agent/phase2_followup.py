from utils import model, extract_json
import json

def post_analysis_and_followup(patient_data):
    prompt = f"""
You are a medical assistant reviewing the following patient data:

{json.dumps(patient_data, indent=2)}

🎯 TASK:
- Carefully analyze the above patient data.
- Identify if any *critical required* medical details are missing, inconsistent, or unclear.
- Do NOT ask unnecessary or overly detailed questions.
- Ask only *essential follow-up questions* one at a time to complete missing key information.
- If the data is sufficient and complete for medical intake purposes, return a JSON with status: "finalized".
- After collecting all required info, return JSON like:
{{
  "updated_patient_data": {{ ... }},
  "notes": "Summary of what was added or clarified",
  "status": "finalized"
}}

Begin your focused analysis now.
"""

    response = model.start_chat(history=[])
    reply = response.send_message(prompt)
    updated_data = dict(patient_data)

    while True:
        if "```json" in reply.text or "{" in reply.text:
            result = extract_json(reply.text)
            if result.get("status") == "finalized":
                return result.get("updated_patient_data", updated_data), result.get("notes", "")
        
        print(f"\n🤖 {reply.text.strip()}")
        user_input = ""
        while not user_input:
            user_input = input("👤 ").strip()
            if not user_input:
                print("⚠️ Please enter a valid response (cannot be empty).")
        reply = response.send_message(user_input)
