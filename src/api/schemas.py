# src/api/schemas.py
from pydantic import BaseModel
from typing import Optional

class InputRecord(BaseModel):
    age: Optional[int]
    job: Optional[str]
    marital: Optional[str]
    education: Optional[str]
    default: Optional[str]
    balance: Optional[float]
    housing: Optional[str]
    loan: Optional[str]
    contact: Optional[str]
    day: Optional[int]
    month: Optional[str]
    duration: Optional[int]
    campaign: Optional[int]
    pdays: Optional[int]
    previous: Optional[int]
    poutcome: Optional[str]
