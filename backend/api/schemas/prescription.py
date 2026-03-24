from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class HerbItem(BaseModel):
    herb_name: str
    dosage_g: float
    processing: Optional[str] = None
    notes: Optional[str] = None

class PrescriptionCreate(BaseModel):
    visit_id: str
    classic_formula_name: Optional[str] = None
    modification_notes: Optional[str] = None
    cooking_instructions: Optional[str] = None
    doses: int = 7
    internal_notes: Optional[str] = None
    patient_notes: Optional[str] = None
    herbs: List[HerbItem] = []

class PrescriptionResponse(BaseModel):
    id: str
    visit_id: str
    classic_formula_name: Optional[str] = None
    modification_notes: Optional[str] = None
    cooking_instructions: Optional[str] = None
    doses: int
    herbs: List[HerbItem] = []
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ClassicFormulaHerbItem(BaseModel):
    herb_name: str
    dosage_liang: Optional[float] = None
    dosage_g: Optional[float] = None
    processing: Optional[str] = None
    notes: Optional[str] = None

    class Config:
        from_attributes = True

class ClassicFormulaResponse(BaseModel):
    id: str
    name: str
    source: Optional[str] = None
    indication: Optional[str] = None
    syndrome: Optional[str] = None
    cooking_notes: Optional[str] = None
    herbs: List[ClassicFormulaHerbItem] = []

    class Config:
        from_attributes = True
