import json
from booking import main as book_appointment

def agent_booking(state, config):
    with open("patient_data.json", "r") as f:
        patient_data = json.load(f)

    appointment_details = book_appointment()
    state["booking_done"] = True
    state["appointment_details"] = appointment_details

    return state
