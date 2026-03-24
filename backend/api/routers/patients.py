from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional
from core.database import get_db
from api.models.patient import Patient
from api.models.visit import Visit
from api.schemas.patient import PatientCreate, PatientUpdate, PatientResponse

router = APIRouter(prefix="/patients", tags=["患者管理"])

@router.post("/", response_model=PatientResponse, summary="新建患者")
async def create_patient(data: PatientCreate, db: AsyncSession = Depends(get_db)):
    patient = Patient(**data.model_dump())
    db.add(patient)
    await db.flush()
    await db.refresh(patient)
    result = PatientResponse.model_validate(patient)
    result.visit_count = 0
    return result

@router.get("/", summary="获取患者列表")
async def list_patients(
    search: Optional[str] = Query(None, description="按姓名或电话搜索"),
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db)
):
    q = select(Patient).where(Patient.is_active == 1)
    if search:
        q = q.where(
            (Patient.name.contains(search)) | (Patient.phone.contains(search))
        )
    q = q.order_by(Patient.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(q)
    patients = result.scalars().all()

    out = []
    for p in patients:
        cnt_q = select(func.count()).where(Visit.patient_id == p.id)
        cnt_r = await db.execute(cnt_q)
        cnt = cnt_r.scalar() or 0
        pr = PatientResponse.model_validate(p)
        pr.visit_count = cnt
        out.append(pr)
    return {"total": len(out), "patients": out}

@router.get("/{patient_id}", response_model=PatientResponse, summary="获取患者详情")
async def get_patient(patient_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Patient).where(Patient.id == patient_id))
    patient = result.scalar_one_or_none()
    if not patient:
        raise HTTPException(status_code=404, detail="患者不存在")
    cnt_q = select(func.count()).where(Visit.patient_id == patient_id)
    cnt_r = await db.execute(cnt_q)
    pr = PatientResponse.model_validate(patient)
    pr.visit_count = cnt_r.scalar() or 0
    return pr

@router.put("/{patient_id}", response_model=PatientResponse, summary="更新患者信息")
async def update_patient(patient_id: str, data: PatientUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Patient).where(Patient.id == patient_id))
    patient = result.scalar_one_or_none()
    if not patient:
        raise HTTPException(status_code=404, detail="患者不存在")
    update_data = data.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        setattr(patient, k, v)
    await db.flush()
    await db.refresh(patient)
    return PatientResponse.model_validate(patient)
