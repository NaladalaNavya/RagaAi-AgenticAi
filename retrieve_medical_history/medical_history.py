from typing import Dict, Any
from db import get_db_connection
import pymysql


def retrieve_medical_history(patient_id: int) -> Dict[str, Any]:
    """
    Retrieve medical history records for a given patient ID.

    Args:
        patient_id (int): The ID of the patient.

    Returns:
        dict: A dictionary with either the medical history records or a message.
    """
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM medical_history WHERE patient_id = %s"
        cursor.execute(query, (patient_id,))
        history = cursor.fetchall()

        if not history:
            return {"medical_history": [], "message": "No previous medical history found for this patient."}
        return {"medical_history": history}

    except pymysql.MySQLError as e:
        return {"error": f"Database error: {str(e)}"}

    finally:
        if conn:
            conn.close()
