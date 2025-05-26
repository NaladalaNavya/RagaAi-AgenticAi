import pymysql
from typing import Optional, List
from pydantic import BaseModel, EmailStr, ValidationError
import json
import sys
from datetime import datetime

class PatientSchema(BaseModel):
    name: str
    email: EmailStr
    age: int
    gender: str
    weight: Optional[int]
    contact: Optional[str]
    address: Optional[str]
    symptoms: List[str] = []
    symptom_duration: Optional[str]
    disease: Optional[str]
    disease_duration: Optional[str]
    medications: List[str] = []
    allergies: List[str] = []
    past_history: Optional[str]
    past_illness_time: Optional[str]
    procedure_name: Optional[str]
    surgery_date: Optional[str]
    hospital_name: Optional[str]
    onset_date: Optional[str] = None
    severity: Optional[str] = None
    past_illness_notes: Optional[str] = None

def preprocess_data(raw_data: dict) -> dict:
    def str_to_list(s):
        if not s:
            return []
        return [item.strip() for item in s.split(",") if item.strip()]

    processed = {
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
    return processed

def parse_date_or_none(date_str: Optional[str]) -> Optional[str]:
    if not date_str:
        return None
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return dt.strftime("%Y-%m-%d")
    except ValueError:
        return None

def format_and_store_data_from_file(file_path: str):
    try:
        with open(file_path, "r") as f:
            raw_input = f.read()
    except FileNotFoundError:
        return {"error": f"❌ File not found: {file_path}"}
    except Exception as e:
        return {"error": f"❌ Failed to read file: {str(e)}"}

    try:
        raw_data = json.loads(raw_input)
    except json.JSONDecodeError:
        return {"error": "❌ Invalid JSON format"}

    processed_data = preprocess_data(raw_data)

    try:
        validated = PatientSchema(**processed_data)
    except ValidationError as e:
        return {"error": e.errors()}

    conn = None
    try:
        conn = pymysql.connect(host='localhost', user='root', password='Navya@2307', db='hospital_system')
        cursor = conn.cursor()
        print("✅ Connected to MySQL")

        print("👉 Inserting patient...")
        cursor.execute("""
            INSERT INTO patients 
            (full_name, email, age, gender, phone, address) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            validated.name,
            validated.email,
            validated.age,
            validated.gender,
            validated.contact,
            validated.address
        ))
        print("✅ Patient inserted.")
        patient_id = cursor.lastrowid

        # Insert symptoms
        for symptom in validated.symptoms:
            cursor.execute("""
                           INSERT INTO symptoms (patient_id, symptom_description, onset_date, severity) 
                           VALUES (%s, %s, %s, %s)
                           """, (
                               patient_id,
                               symptom,
                               parse_date_or_none(validated.onset_date),
                               validated.severity
                               ))

        # Insert allergies
        for allergy in validated.allergies:
            cursor.execute("""
                INSERT INTO allergies (patient_id, substance) 
                VALUES (%s, %s)
            """, (patient_id, allergy))

        # Insert medications
        for med in validated.medications:
            cursor.execute("""
                INSERT INTO medications (patient_id, medication_name) 
                VALUES (%s, %s)
            """, (patient_id, med))

        # Insert medical history
        if validated.past_history:
            diagnosis_date = parse_date_or_none(validated.past_illness_time)
            notes = None
            if not diagnosis_date and validated.past_illness_time:
                notes = validated.past_illness_time

            cursor.execute("""
                INSERT INTO medical_history 
                (patient_id, `condition`, diagnosis_date, notes, is_chronic)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                patient_id,
                validated.past_history,
                diagnosis_date,
                notes,
                1  # Assuming chronic for demo
            ))

        # Insert surgery (note the correct table name: surgeries)
        if validated.procedure_name and validated.surgery_date:
            cursor.execute("""
                INSERT INTO surgeries 
                (patient_id, procedure_name, surgery_date, hospital_name)
                VALUES (%s, %s, %s, %s)
            """, (
                patient_id,
                validated.procedure_name,
                parse_date_or_none(validated.surgery_date),
                validated.hospital_name
            ))

        conn.commit()
        print("✅ All data committed to the database.")
        return {"structured_data": processed_data, "patient_id": patient_id}

    except Exception as db_err:
        return {"error": f"❌ Database error: {str(db_err)}"}
    finally:
        if conn:
            conn.close()
            print("🔒 Connection closed.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Please provide the path to the JSON file.")
    else:
        file_path = sys.argv[1]
        result = format_and_store_data_from_file(file_path)
        print("📦 Final Result:", result)
