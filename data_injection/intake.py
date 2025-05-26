def collect_patient_data():
    print("👨‍⚕️ Medical Intake Chatbot: Hello! Let's quickly collect your basic medical details.\n")
    patient_data = {}

    questions = [
        ("name", "What is your full name?"),
        ("email", "Your email address?"),
        ("age", "How old are you?"),
        ("gender", "Your gender? (M/F/Other)"),
        ("weight", "Your weight in kg?"),
        ("Ph Number", "What is your contact number?"),
        ("Address", "What is your address?")
    ]

    for key, question in questions:
        patient_data[key] = input(f"🧑 {question} ").strip()

    def follow_up_if_yes(key, main_question, follow_ups):
        response = input(f"🧑 {main_question} ").strip().lower()
        patient_data[key] = response
        if response in ["yes", "y"]:
            for f_key, f_q in follow_ups:
                patient_data[f_key] = input(f"🧑 {f_q} ").strip()

    follow_up_if_yes("symptoms", "Do you have any symptoms? (Yes/No)", [
        ("symptom_list", "What symptoms are you experiencing?"),
        ("onset_date", "When did the symptoms start? (YYYY-MM-DD)"),
        ("severity", "How severe are the symptoms? (mild/moderate/severe)")
    ])

    follow_up_if_yes("disease", "Do you have any known diseases? (Yes/No)", [
        ("disease_name", "Which disease(s)?"),
        ("disease_duration", "Since when?")
    ])

    follow_up_if_yes("medications", "Are you taking any medications? (Yes/No)", [
        ("medication_list", "Please list the medications.")
    ])

    follow_up_if_yes("allergies", "Do you have any allergies? (Yes/No)", [
        ("allergy_list", "Please list substances you're allergic to (comma separated):"),
        ("severity", "How severe are the allergies? (mild/moderate/severe)")
    ])

    follow_up_if_yes("past_history", "Any past major illness or surgery? (Yes/No)", [
        ("past_illness", "Please describe the illness or surgery."),
        ("past_illness_time", "When did it happen? (YYYY-MM-DD)"),
        ("procedure_name", "What was the surgical procedure (if any)?"),
        ("surgery_date", "What was the surgery date? (YYYY-MM-DD)"),
        ("hospital_name", "Where was the surgery performed?")
    ])

    return patient_data
