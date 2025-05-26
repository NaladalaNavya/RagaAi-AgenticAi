from typing import Optional, List
from pydantic import BaseModel, EmailStr

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
