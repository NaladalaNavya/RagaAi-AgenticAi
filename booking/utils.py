def parse_available_days(days_str):
    days_str = days_str.strip().lower()
    day_map = {
        "mon": "Monday",
        "tue": "Tuesday",
        "wed": "Wednesday",
        "thu": "Thursday",
        "fri": "Friday",
        "sat": "Saturday",
        "sun": "Sunday"
    }

    if "-" in days_str:
        start, end = [d.strip() for d in days_str.split("-")]
        keys = list(day_map.keys())
        start_idx = keys.index(start)
        end_idx = keys.index(end)
        if end_idx < start_idx:
            end_idx += 7
        return [day_map[keys[i % 7]] for i in range(start_idx, end_idx + 1)]
    else:
        parts = [d.strip() for d in days_str.split(",")]
        return [day_map.get(p, "") for p in parts if p in day_map]

def get_patient_id_by_email(cursor, email):
    cursor.execute("SELECT patient_id FROM patients WHERE email = %s", (email,))
    result = cursor.fetchone()
    return result['patient_id'] if result else None
