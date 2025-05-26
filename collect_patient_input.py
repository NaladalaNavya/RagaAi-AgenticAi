import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variable
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("API key not found. Please set GOOGLE_API_KEY in your environment.")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# Optional: LLM post-processing to clean/validate
def extract_structured_summary(data: dict) -> str:
    prompt = (
        "Format the following patient data into a clean JSON structure for storage:\n\n"
        f"{json.dumps(data, indent=2)}"
    )
    return model.generate_content(prompt).text.strip()

# Main intake function
def collect_patient_input():
    print("👨‍⚕️ Medical Intake Chatbot: Hello! Let's quickly collect your basic medical details.\n")

    patient_data = {}

    # Basic questions
    questions = [
        ("name", "What is your full name?"),
        ("email", "Your email address?"),
        ("age", "How old are you?"),
        ("gender", "Your gender? (M/F/Other)"),
        ("weight", "Your weight in kg?"),
        ("Ph Number", " What is your contact number?"),
        ("Address", "What is your address?")
    ]

    for key, question in questions:
        answer = input(f"🧑 {question} ").strip()
        patient_data[key] = answer

    # Conditional health-related questions
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

    # Save raw data
    with open("patient_summary.json", "w", encoding="utf-8") as f:
        json.dump(patient_data, f, indent=2)
    print("✅ Your details have been saved in 'patient_summary.json'.")

    # Optional: clean up with LLM
    try:
        summary = extract_structured_summary(patient_data)
        with open("patient_summary_llm.json", "w", encoding="utf-8") as f:
            f.write(summary)
        print("✅ LLM-processed summary saved in 'patient_summary_llm.json'.")
    except Exception as e:
        print(f"⚠️ Could not generate LLM summary: {str(e)}")

if __name__ == "__main__":
    collect_patient_input()
