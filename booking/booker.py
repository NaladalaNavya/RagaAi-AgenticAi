import json
from datetime import datetime, timedelta
from db import connect_to_db
from utils import parse_available_days, get_patient_id_by_email

def book_appointment(summary_path):
    with open(summary_path) as f:
        data = json.load(f)

    recommended_specialists = data.get("recommended_specialist", [])
    patient_email = data["patient_data"].get("email")

    if not patient_email:
        print("❌ Patient email not found in JSON.")
        return

    conn = connect_to_db()
    cursor = conn.cursor(dictionary=True)

    try:
        patient_id = get_patient_id_by_email(cursor, patient_email)
        if not patient_id:
            print(f"❌ Patient with email {patient_email} not found.")
            return

        for specialist in recommended_specialists:
            print(f"Looking for doctors specializing in: {specialist}")
            cursor.execute("SELECT * FROM doctors WHERE specialization = %s", (specialist,))
            doctors = cursor.fetchall()

            if not doctors:
                print(f"⚠️ No doctors found for specialization: {specialist}")
                continue

            for doctor in doctors:
                available_days = parse_available_days(doctor["available_days"])
                try:
                    available_slots = json.loads(doctor["available_slots"])
                except Exception as e:
                    print(f"❌ Slot parsing error for Dr. {doctor['full_name']}: {e}")
                    continue

                for i in range(7):
                    check_date = datetime.today() + timedelta(days=i)
                    weekday = check_date.strftime('%A')

                    if weekday in available_days:
                        for slot in available_slots:
                            slot_time = slot if len(slot) == 8 else slot + ":00"

                            cursor.execute("""
                                SELECT 1 FROM appointments
                                WHERE doctor_id = %s AND appointment_date = %s AND appointment_time = %s
                            """, (doctor["doctor_id"], check_date.date(), slot_time))

                            if not cursor.fetchone():
                                cursor.execute("""
                                    INSERT INTO appointments
                                    (patient_id, doctor_id, appointment_date, appointment_time, status)
                                    VALUES (%s, %s, %s, %s, %s)
                                """, (patient_id, doctor["doctor_id"], check_date.date(), slot_time, 1))
                                conn.commit()
                                print(f"✅ Booked with Dr. {doctor['full_name']} on {check_date.date()} at {slot_time}")
                                return
        print("❌ No available slots found in the next 7 days.")

    finally:
        cursor.close()
        conn.close()
