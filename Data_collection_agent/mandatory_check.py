from config import model
from utils import extract_json
import json

def confirm_mandatory_fields(final_json):
    prompt = f"""
You are a medical assistant. 

Given the patient data JSON below, check if ALL mandatory fields are present.

Mandatory fields:

- From Patient: "name" (maps to full_name), "email", "age", "gender", "Ph Number" (phone), "Address" (address)
- If "symptoms" == "yes": "symptom_list" required (comma-separated string)
- If "allergies" == "yes": "allergy_list" required
- If "medications" == "yes": "medication_list" required
- If "past_history" == "yes": "past_illness" required
- If surgery info present: "procedure_name", "surgery_date", "hospital_name" required

If any mandatory fields are missing or empty, ask the patient directly to provide them one by one.

If all mandatory fields are present, reply with:

{{"status": "confirmed", "message": "All mandatory fields present."}}

Otherwise, ask only for missing fields one at a time.

Here is the patient data:

{json.dumps(final_json, indent=2)}

Begin your check and ask for missing info as needed.
"""

    response = model.start_chat(history=[])
    reply = response.send_message(prompt)

    updated_data = dict(final_json)

    while True:
        print(f"\n🤖 {reply.text.strip()}")
        output = extract_json(reply.text)

        if output.get("status") == "confirmed":
            print("✅ Mandatory fields confirmed complete.")
            return updated_data

        user_input = ""
        while not user_input:
            user_input = input("👤 ").strip()
            if not user_input:
                print("⚠️ Please provide a valid response.")

        last_bot_msg = reply.text.lower()

        if "name" in last_bot_msg:
            updated_data["patient_data"]["name"] = user_input
        elif "email" in last_bot_msg:
            updated_data["patient_data"]["email"] = user_input
        elif "age" in last_bot_msg:
            updated_data["patient_data"]["age"] = user_input
        elif "gender" in last_bot_msg:
            updated_data["patient_data"]["gender"] = user_input
        elif "phone" in last_bot_msg or "ph number" in last_bot_msg:
            updated_data["patient_data"]["phone"] = user_input
        elif "address" in last_bot_msg:
            updated_data["patient_data"]["address"] = user_input
        else:
            # fallback: add to generic patient_data
            updated_data["patient_data"]["additional_info"] = user_input

        reply = response.send_message(user_input)
