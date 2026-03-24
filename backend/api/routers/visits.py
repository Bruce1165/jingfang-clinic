from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from datetime import datetime, timedelta
import json
from core.database import get_db
from core.config import settings
from api.models.visit import Visit, EfficacyEnum
from api.models.patient import Patient

router = APIRouter(prefix="/visits", tags=["就诊记录"])

from pydantic import BaseModel
from datetime import date

class VisitCreate(BaseModel):
    patient_id: str
    visit_number: Optional[int] = None
    chief_complaint: Optional[str] = None
    present_illness: Optional[str] = None
    inquiry_notes: Optional[str] = None
    doctor_notes: Optional[str] = None
    tongue_color: Optional[str] = None
    tongue_coating: Optional[str] = None
    tongue_coating_texture: Optional[str] = None
    tongue_shape: Optional[str] = None
    pulse_data: Optional[dict] = None
    symptoms_structured: Optional[dict] = None
    syndrome_cold_heat: Optional[str] = None
    syndrome_xu_shi: Optional[str] = None
    six_channel: Optional[str] = None
    days_of_medicine: Optional[int] = 7

class EfficacyUpdate(BaseModel):
    efficacy: EfficacyEnum
    efficacy_notes: Optional[str] = None

@router.post("/", summary="新建就诊记录")
async def create_visit(data: VisitCreate, db: AsyncSession = Depends(get_db)):
    # 自动计算第几诊
    from sqlalchemy import func
    cnt_q = select(func.count()).where(Visit.patient_id == data.patient_id)
    cnt_r = await db.execute(cnt_q)
    visit_number = (cnt_r.scalar() or 0) + 1

    visit = Visit(
        patient_id=data.patient_id,
        visit_number=data.visit_number or visit_number,
        chief_complaint=data.chief_complaint,
        present_illness=data.present_illness,
        inquiry_notes=data.inquiry_notes,
        doctor_notes=data.doctor_notes,
        tongue_color=data.tongue_color,
        tongue_coating=data.tongue_coating,
        tongue_coating_texture=data.tongue_coating_texture,
        tongue_shape=data.tongue_shape,
        pulse_data=json.dumps(data.pulse_data, ensure_ascii=False) if data.pulse_data else None,
        symptoms_structured=json.dumps(data.symptoms_structured, ensure_ascii=False) if data.symptoms_structured else None,
        syndrome_cold_heat=data.syndrome_cold_heat,
        syndrome_xu_shi=data.syndrome_xu_shi,
        six_channel=data.six_channel,
        days_of_medicine=data.days_of_medicine,
        next_visit_date=datetime.now().date() + timedelta(days=data.days_of_medicine or settings.DEFAULT_VISIT_DAYS),
    )
    db.add(visit)
    await db.flush()
    await db.refresh(visit)
    return {"id": visit.id, "visit_number": visit.visit_number, "next_visit_date": str(visit.next_visit_date)}

@router.get("/patient/{patient_id}", summary="获取患者所有就诊记录")
async def get_patient_visits(patient_id: str, db: AsyncSession = Depends(get_db)):
    q = select(Visit).where(Visit.patient_id == patient_id).order_by(Visit.visit_date.desc())
    result = await db.execute(q)
    visits = result.scalars().all()
    return [{"id": v.id, "visit_number": v.visit_number, "visit_date": str(v.visit_date),
             "chief_complaint": v.chief_complaint, "six_channel": v.six_channel,
             "efficacy": v.efficacy, "days_of_medicine": v.days_of_medicine,
             "next_visit_date": str(v.next_visit_date) if v.next_visit_date else None} for v in visits]

@router.get("/{visit_id}", summary="获取就诊详情")
async def get_visit(visit_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Visit).where(Visit.id == visit_id))
    visit = result.scalar_one_or_none()
    if not visit:
        raise HTTPException(status_code=404, detail="记录不存在")
    return {
        "id": visit.id, "patient_id": visit.patient_id,
        "visit_number": visit.visit_number, "visit_date": str(visit.visit_date),
        "chief_complaint": visit.chief_complaint, "present_illness": visit.present_illness,
        "inquiry_notes": visit.inquiry_notes, "doctor_notes": visit.doctor_notes,
        "tongue_color": visit.tongue_color, "tongue_coating": visit.tongue_coating,
        "tongue_coating_texture": visit.tongue_coating_texture, "tongue_shape": visit.tongue_shape,
        "pulse_data": json.loads(visit.pulse_data) if visit.pulse_data else None,
        "symptoms_structured": json.loads(visit.symptoms_structured) if visit.symptoms_structured else None,
        "syndrome_cold_heat": visit.syndrome_cold_heat, "syndrome_xu_shi": visit.syndrome_xu_shi,
        "six_channel": visit.six_channel, "efficacy": visit.efficacy,
        "efficacy_notes": visit.efficacy_notes, "days_of_medicine": visit.days_of_medicine,
        "next_visit_date": str(visit.next_visit_date) if visit.next_visit_date else None,
    }

@router.patch("/{visit_id}/efficacy", summary="更新疗效评估")
async def update_efficacy(visit_id: str, data: EfficacyUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Visit).where(Visit.id == visit_id))
    visit = result.scalar_one_or_none()
    if not visit:
        raise HTTPException(status_code=404, detail="记录不存在")
    visit.efficacy = data.efficacy
    visit.efficacy_notes = data.efficacy_notes
    await db.flush()
    return {"status": "ok", "efficacy": visit.efficacy}
