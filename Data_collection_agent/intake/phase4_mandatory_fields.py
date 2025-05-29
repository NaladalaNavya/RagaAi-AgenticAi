from intake.utils import model, extract_json
import json

def confirm_mandatory_fields(final_json):
    prompt = f\"\"\"You are a medical assistant. 
    (Same instructions for mandatory fields checking)
    \"\"\"

    response = model.start_chat(history=[])
    reply = response.send_message(prompt)
    updated_data = dict(final_json)

    while True:
        print(f"\n🤖 {reply.text.strip()}")
        output = extract_json(reply.text)
        if output.get("status") == "confirmed":
            return updated_data

        user_input = input("👤 ").strip()
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
