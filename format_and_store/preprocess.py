from utils import str_to_list

def preprocess_data(raw_data: dict) -> dict:
    return {
        "name": raw_data.get("name"),
        "email": raw_data.get("email"),
        "age": int(raw_data.get("age", 0)) if raw_data.get("age") else None,
        "gender": raw_data.get("gender"),
        "weight": int(raw_data.get("weight")) if raw_data.get("weight") else None,
        "contact": raw_data.get("Ph Number"),
        "address": raw_data.get("Address"),
        "symptoms": str_to_list(raw_data.get("symptom_list", "")) if raw_data.get("symptoms", "").lower() in ["yes", "y"] else [],
        "symptom_duration": raw_data.get("symptom_duration"),
        "disease": raw_data.get("disease_name") if raw_data.get("disease", "").lower() in ["yes", "y"] else None,
        "disease_duration": raw_data.get("disease_duration"),
        "medications": str_to_list(raw_data.get("medication_list", "")) if raw_data.get("medications", "").lower() in ["yes", "y"] else [],
        "allergies": str_to_list(raw_data.get("allergy_list", "")) if raw_data.get("allergies", "").lower() in ["yes", "y"] else [],
        "past_history": raw_data.get("past_illness") if raw_data.get("past_history", "").lower() in ["yes", "y"] else None,
        "past_illness_time": raw_data.get("past_illness_time"),
        "procedure_name": raw_data.get("procedure_name"),
        "surgery_date": raw_data.get("surgery_date"),
        "hospital_name": raw_data.get("hospital_name"),
        "onset_date": raw_data.get("onset_date"),
        "severity": raw_data.get("severity"),
        "past_illness_notes": raw_data.get("past_illness_notes"),
    }
