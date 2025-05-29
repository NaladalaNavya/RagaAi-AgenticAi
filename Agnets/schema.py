from typing import TypedDict, Optional, List, Dict

class PatientState(TypedDict):
    patient_data: Optional[dict]
    summary: Optional[str]
    followup_notes: Optional[str]
    recommended_specialist: Optional[List[str]]
    specialist_rationale: Optional[str]
    mapped_json: Optional[List[Dict]]
    db_inserted: bool
    booking_done: bool
    appointment_details: Optional[dict]
