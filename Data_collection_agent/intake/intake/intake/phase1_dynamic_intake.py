from intake.utils import model, extract_json

def dynamic_medical_intake():
    intro = \"\"\"You are an intelligent medical intake assistant...
    (trimmed for brevity — same intro content as before)
    \"\"\"

    response = model.start_chat(history=[])
    reply = response.send_message(intro + "\n\nStart by asking the first question to the patient.")

    patient_data = {}
    while True:
        print(f"\n🤖 {reply.text.strip()}")
        user_input = ""
        while not user_input:
            user_input = input("👤 ").strip()

        reply = response.send_message(user_input)
        final_output = extract_json(reply.text)
        if final_output.get("status") == "complete":
            return final_output.get("patient_data", {}), final_output.get("summary", "")
