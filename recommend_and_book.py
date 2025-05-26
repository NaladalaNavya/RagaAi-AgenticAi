import pymysql
from datetime import datetime, timedelta

def recommend_doctor_and_book(patient_id, specialization, preferred_date=None, preferred_time=None):
    """
    Recommend a doctor based on specialization and book an appointment.

    Args:
        patient_id (int): Patient ID
        specialization (str): Doctor specialization required
        preferred_date (str or None): Preferred appointment date 'YYYY-MM-DD', optional
        preferred_time (str or None): Preferred appointment time 'HH:MM:SS', optional

    Returns:
        dict: Contains booking confirmation or error message
    """
    conn = pymysql.connect(host='localhost', user='root', password='Navya@2307', db='hospital_system')
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # If no preferred_date, choose next available date from today
    if not preferred_date:
        preferred_date = datetime.now().strftime('%Y-%m-%d')

    # Step 1: Find doctors by specialization
    cursor.execute("""
        SELECT doctor_id, full_name FROM doctors WHERE specialization = %s
    """, (specialization,))
    doctors = cursor.fetchall()

    if not doctors:
        conn.close()
        return {"error": f"No doctors found with specialization '{specialization}'"}

    # Step 2: Find availability of these doctors on preferred_date
    doctor_ids = [doc['doctor_id'] for doc in doctors]
    format_ids = ",".join(str(did) for did in doctor_ids)

    cursor.execute(f"""
        SELECT * FROM doctor_availability 
        WHERE doctor_id IN ({format_ids}) AND available_date = %s
        ORDER BY start_time
    """, (preferred_date,))

    availabilities = cursor.fetchall()
    if not availabilities:
        conn.close()
        return {"error": f"No availability for doctors specialized in '{specialization}' on {preferred_date}"}

    # Step 3: Choose the first available slot (or preferred time if given)
    chosen_slot = None
    for slot in availabilities:
        if preferred_time:
            # Check if preferred time fits in slot
            if slot['start_time'] <= preferred_time <= slot['end_time']:
                chosen_slot = slot
                break
        else:
            chosen_slot = slot
            break

    if not chosen_slot:
        conn.close()
        return {"error": "No suitable time slot found"}

    # Step 4: Book the appointment: insert into appointments
    appointment_date = chosen_slot['available_date']
    appointment_time = preferred_time if preferred_time else chosen_slot['start_time']
    doctor_id = chosen_slot['doctor_id']

    # Check if slot is already booked (optional: check existing confirmed appointment)
    cursor.execute("""
        SELECT * FROM appointments 
        WHERE doctor_id = %s AND appointment_date = %s AND appointment_time = %s AND confirmed = 1
    """, (doctor_id, appointment_date, appointment_time))

    existing = cursor.fetchone()
    if existing:
        conn.close()
        return {"error": "Chosen time slot is already booked"}

    cursor.execute("""
        INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time, confirmed) 
        VALUES (%s, %s, %s, %s, %s)
    """, (patient_id, doctor_id, appointment_date, appointment_time, 1))

    conn.commit()
    appointment_id = cursor.lastrowid
    conn.close()

    return {
        "message": "Appointment successfully booked",
        "appointment_id": appointment_id,
        "patient_id": patient_id,
        "doctor_id": doctor_id,
        "appointment_date": appointment_date.strftime('%Y-%m-%d') if isinstance(appointment_date, datetime) else appointment_date,
        "appointment_time": str(appointment_time)
    }


# Example usage
if __name__ == "__main__":
    patient_id = 12  # replace with actual patient_id
    specialization = "Neurologist"
    preferred_date = None  # or '2025-06-01'
    preferred_time = None  # or '14:30:00'

    result = recommend_doctor_and_book(patient_id, specialization, preferred_date, preferred_time)
    print(result)
