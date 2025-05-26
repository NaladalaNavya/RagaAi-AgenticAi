import pymysql
def retrieve_history(state):
    patient_id = state["patient_id"]
    conn = pymysql.connect(host='localhost', user='root', password='Navya@2307', db='hospital_system')
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    cursor.execute("SELECT * FROM medical_history WHERE patient_id = %s", (patient_id,))
    history = cursor.fetchall()

    conn.close()

    if not history:
        return {"medical_history": [], "message": "No previous medical history found for this patient."}
    else:
        return {"medical_history": history}


if __name__ == "__main__":
    # Example state dict with a patient_id (use a valid patient_id from your DB)
    state = {"patient_id": 21}

    result = retrieve_history(state)
    print(result)
