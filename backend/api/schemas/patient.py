from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime
from enum import Enum

class GenderEnum(str, Enum):
    male = "male"
    female = "female"
    other = "other"

class PatientCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    gender: GenderEnum
    birth_date: Optional[date] = None
    age: Optional[int] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    bazi_year: Optional[str] = None
    bazi_month: Optional[str] = None
    bazi_day: Optional[str] = None
    bazi_hour: Optional[str] = None
    birth_hour_raw: Optional[str] = None
    constitution_hint: Optional[str] = None
    notes: Optional[str] = None

class PatientUpdate(PatientCreate):
    name: Optional[str] = None
    gender: Optional[GenderEnum] = None

class PatientResponse(BaseModel):
    id: str
    name: str
    gender: GenderEnum
    birth_date: Optional[date] = None
    age: Optional[int] = None
    phone: Optional[str] = None
    bazi_year: Optional[str] = None
    bazi_month: Optional[str] = None
    bazi_day: Optional[str] = None
    bazi_hour: Optional[str] = None
    birth_hour_raw: Optional[str] = None
    constitution_hint: Optional[str] = None
    notes: Optional[str] = None
    created_at: Optional[datetime] = None
    visit_count: Optional[int] = 0

    class Config:
        from_attributes = True
