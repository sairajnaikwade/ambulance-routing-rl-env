from pydantic import BaseModel
from typing import List

class Patient(BaseModel):
    location: int
    severity: float
    time_left: float

class Hospital(BaseModel):
    location: int
    capacity: int

class AmbulanceState(BaseModel):
    ambulance_location: int
    patients: List[Patient]
    hospitals: List[Hospital]
    traffic: List[List[float]]

class AmbulanceAction(BaseModel):
    target_type: str
    target_id: int

class AmbulanceObservation(BaseModel):
    ambulance_location: int
    patients: List[Patient]
    hospitals: List[Hospital]