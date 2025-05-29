from utils import model, extract_json
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
            return updated_data

        user_input = ""
        while not user_input:
            user_input = input("👤 ").strip()
            if not user_input:
                print("⚠️ Please provide a valid response.")
        
        last_msg = reply.text.lower()

        pd = updated_data["patient_data"]
        if "name" in last_msg:
            pd["name"] = user_input
        elif "email" in last_msg:
            pd["email"] = user_input
        elif "age" in last_msg:
            pd["age"] = int(user_input) if user_input.isdigit() else user_input
        elif "gender" in last_msg:
            pd["gender"] = user_input
        elif "phone" in last_msg:
            pd["phone"] = user_input
        elif "address" in last_msg:
            pd["address"] = user_input
        elif "symptom" in last_msg:
            pd["symptoms"] = "yes"
            pd["symptom_list"] = user_input
        elif "allergy" in last_msg:
            pd["allergies"] = "yes"
            pd["allergy_list"] = user_input
        elif "medication" in last_msg:
            pd["medications"] = "yes"
            pd["medication_list"] = user_input
        elif "past illness" in last_msg:
            pd["past_history"] = "yes"
            pd["past_illness"] = user_input
        elif "procedure name" in last_msg:
            pd["procedure_name"] = user_input
        elif "surgery date" in last_msg:
            pd["surgery_date"] = user_input
        elif "hospital name" in last_msg:
            pd["hospital_name"] = user_input

        reply = response.send_message(user_input)
