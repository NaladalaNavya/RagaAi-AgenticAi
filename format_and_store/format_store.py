import json
import sys
from pydantic import ValidationError
from config import get_mysql_connection
from schema import PatientSchema
from preprocess import preprocess_data
from utils import parse_date_or_none

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
        conn = get_mysql_connection()
        cursor = conn.cursor()
        print("✅ Connected to MySQL")

        print("👉 Inserting patient...")
        cursor.execute("""
            INSERT INTO patients (full_name, email, age, gender, phone, address)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            validated.name, validated.email, validated.age, validated.gender,
            validated.contact, validated.address
        ))
        patient_id = cursor.lastrowid
        print("✅ Patient inserted.")

        for symptom in validated.symptoms:
            cursor.execute("""
                INSERT INTO symptoms (patient_id, symptom_description, onset_date, severity)
                VALUES (%s, %s, %s, %s)
            """, (patient_id, symptom, parse_date_or_none(validated.onset_date), validated.severity))

        for allergy in validated.allergies:
            cursor.execute("""
                INSERT INTO allergies (patient_id, substance)
                VALUES (%s, %s)
            """, (patient_id, allergy))

        for med in validated.medications:
            cursor.execute("""
                INSERT INTO medications (patient_id, medication_name)
                VALUES (%s, %s)
            """, (patient_id, med))

        if validated.past_history:
            cursor.execute("""
                INSERT INTO medical_history (patient_id, `condition`, diagnosis_date, notes, is_chronic)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                patient_id,
                validated.past_history,
                parse_date_or_none(validated.past_illness_time),
                validated.past_illness_time if not parse_date_or_none(validated.past_illness_time) else None,
                1
            ))

        if validated.procedure_name and validated.surgery_date:
            cursor.execute("""
                INSERT INTO surgeries (patient_id, procedure_name, surgery_date, hospital_name)
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

