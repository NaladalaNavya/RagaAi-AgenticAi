import os
import json
import re
from dotenv import load_dotenv
import google.generativeai as genai

# Load API Key from .env
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("API key not found. Please set GOOGLE_API_KEY in your environment.")
genai.configure(api_key=api_key)

# Initialize Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

# ✅ Input Validators
def validate_email(email): return re.match(r"[^@]+@[^@]+\.[^@]+", email)
def validate_age(age): return age.isdigit() and 0 < int(age) < 120
def validate_phone(phone): return re.match(r"^[0-9\-\+\s\(\)]{10,15}$", phone)
def validate_weight(weight): return weight.replace('.', '', 1).isdigit()

def extract_json(text):
    """Extract the first valid JSON object from LLM output."""
    try:
        json_start = text.find("{")
        json_end = text.rfind("}")
        if json_start != -1 and json_end != -1:
            json_str = text[json_start:json_end+1]
            return json.loads(json_str)
    except Exception as e:
        print("⚠️ Error parsing JSON:", e)
    return {}

# 🧠 Intelligent Agent with Dynamic Reasoning + Follow-ups
def dynamic_medical_analysis(patient_data: dict) -> dict:
    prompt = f"""
You are a clinical AI assistant. Analyze the patient data and output:
1. A clinical summary.
2. Severity level (mild/moderate/severe/critical).
3. Missing or unclear info (ask questions).
4. Recommended medical specialist.
5. Justification for the choice.

Examples:
---
Patient: {{"symptom_list": "chest pain, shortness of breath", "age": "55", "disease_name": "hypertension"}}
Output:
{{
  "condition_summary": "Possible cardiovascular distress with chest pain and history of hypertension.",
  "severity": "moderate",
  "missing_info_questions": [],
  "recommended_specialist": "Cardiologist",
  "reasoning": "Chest-related symptoms and hypertension indicate a heart-related issue."
}}

Patient: {{"symptom_list": "persistent cough, fever", "age": "28"}}
Output:
{{
  "condition_summary": "Symptoms suggest a respiratory infection.",
  "severity": "mild",
  "missing_info_questions": ["Do you have chest pain or difficulty breathing?", "How long have you had the cough?"],
  "recommended_specialist": "Pulmonologist",
  "reasoning": "Respiratory symptoms are best handled by a lung specialist."
}}

Now analyze this patient:
{json.dumps(patient_data, indent=2)}
"""
    try:
        response = model.generate_content(prompt)
        content = response.text.strip()
        print("\n📤 Raw LLM Output:\n", content)  # Debug print
        return extract_json(content)
    except Exception as e:
        print("❌ LLM generation failed:", e)
        return {}

# 🤖 Conversational Intake
def collect_patient_data():
    print("👩‍⚕️ Medical Assistant: Hi! Let's get to know your health condition step by step.\n")
    patient = {}

    def ask(prompt, key, validator=None, err="❌ Invalid input. Please try again."):
        while True:
            ans = input(f"👤 {prompt} ").strip()
            if not validator or validator(ans):
                patient[key] = ans
                return
            print(err)

    ask("What's your full name?", "name")
    ask("Email address?", "email", validate_email, "❌ Invalid email format.")
    ask("Age?", "age", validate_age, "❌ Enter a valid age between 1 and 120.")
    ask("Gender? (M/F/Other)", "gender")
    ask("Weight (kg)?", "weight", validate_weight, "❌ Enter a valid number.")
    ask("Phone number?", "phone", validate_phone, "❌ Invalid phone number.")
    ask("Address?", "address")

    def follow_up_if_yes(key, main_q, subs):
        response = input(f"👤 {main_q} (Yes/No) ").lower()
        patient[key] = response
        if response in ["yes", "y"]:
            for k, q in subs:
                patient[k] = input(f"📝 {q} ").strip()

    follow_up_if_yes("has_symptoms", "Do you currently have any symptoms?", [
        ("symptom_list", "What symptoms are you experiencing?"),
        ("onset_date", "When did the symptoms start? (YYYY-MM-DD)"),
        ("severity", "How severe do you feel they are? (mild/moderate/severe)")
    ])
    follow_up_if_yes("has_disease", "Do you have any known diseases?", [
        ("disease_name", "What disease(s)?"),
        ("disease_duration", "Since when?")
    ])
    follow_up_if_yes("on_medications", "Are you taking any medications currently?", [
        ("medication_list", "List them.")
    ])
    follow_up_if_yes("has_allergies", "Do you have allergies?", [
        ("allergy_list", "List them."),
        ("allergy_severity", "How severe? (mild/moderate/severe)")
    ])
    follow_up_if_yes("past_surgeries", "Any past major illness or surgeries?", [
        ("past_illness", "Describe the condition."),
        ("past_illness_time", "When did it happen?"),
        ("procedure_name", "What procedure?"),
        ("surgery_date", "Date of surgery?"),
        ("hospital_name", "Where was it done?")
    ])

    with open("patient_summary.json", "w") as f:
        json.dump(patient, f, indent=2)
    print("✅ Data saved to 'patient_summary.json'")
    return patient

# 🔁 Feedback Loop: Ask questions model needs answers to
def handle_follow_ups(analysis, patient_data):
    if analysis.get("missing_info_questions"):
        print("\n🤖 I need a few more details:")
        for question in analysis["missing_info_questions"]:
            response = input(f"🧠 {question} ").strip()
            patient_data[question] = response
        print("🔄 Re-analyzing with updated inputs...\n")
        return dynamic_medical_analysis(patient_data)
    return analysis

# 🚀 Run All
def run_pipeline():
    patient_data = collect_patient_data()
    print("\n🩺 Analyzing your symptoms...")
    analysis = dynamic_medical_analysis(patient_data)
    analysis = handle_follow_ups(analysis, patient_data)

    print("\n📋 Final Report:")
    print(json.dumps(analysis, indent=2))
    with open("patient_final_analysis.json", "w") as f:
        json.dump(analysis, f, indent=2)
    print("\n✅ Analysis saved to 'patient_final_analysis.json'")

if __name__ == "__main__":
    run_pipeline()
