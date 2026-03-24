from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.database import get_db
from api.models.prescription import Prescription, PrescriptionHerb, ClassicFormula, ClassicFormulaHerb
from api.schemas.prescription import PrescriptionCreate, PrescriptionResponse, ClassicFormulaResponse
from typing import Optional

router = APIRouter(prefix="/prescriptions", tags=["处方管理"])

@router.post("/", summary="保存处方")
async def create_prescription(data: PrescriptionCreate, db: AsyncSession = Depends(get_db)):
    rx = Prescription(
        visit_id=data.visit_id,
        classic_formula_name=data.classic_formula_name,
        modification_notes=data.modification_notes,
        cooking_instructions=data.cooking_instructions,
        doses=data.doses,
        internal_notes=data.internal_notes,
        patient_notes=data.patient_notes,
    )
    db.add(rx)
    await db.flush()

    for h in data.herbs:
        herb = PrescriptionHerb(
            prescription_id=rx.id,
            herb_name=h.herb_name,
            dosage_g=h.dosage_g,
            dosage_liang=round(h.dosage_g / 5.0, 2),
            processing=h.processing,
            notes=h.notes,
        )
        db.add(herb)
    await db.flush()
    await db.refresh(rx)
    return {"id": rx.id, "status": "saved"}

@router.get("/visit/{visit_id}", summary="获取就诊处方")
async def get_visit_prescription(visit_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Prescription).where(Prescription.visit_id == visit_id)
        .order_by(Prescription.created_at.desc())
    )
    rxs = result.scalars().all()
    out = []
    for rx in rxs:
        h_result = await db.execute(
            select(PrescriptionHerb).where(PrescriptionHerb.prescription_id == rx.id)
        )
        herbs = h_result.scalars().all()
        out.append({
            "id": rx.id, "classic_formula_name": rx.classic_formula_name,
            "modification_notes": rx.modification_notes,
            "cooking_instructions": rx.cooking_instructions,
            "doses": rx.doses, "internal_notes": rx.internal_notes,
            "patient_notes": rx.patient_notes,
            "herbs": [{"herb_name": h.herb_name, "dosage_g": h.dosage_g,
                       "dosage_liang": h.dosage_liang, "processing": h.processing} for h in herbs],
        })
    return out

@router.get("/visit/{visit_id}/print", summary="处方打印版本")
async def print_prescription(visit_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Prescription).where(Prescription.visit_id == visit_id)
        .order_by(Prescription.created_at.desc())
    )
    rx = result.scalars().first()
    if not rx:
        raise HTTPException(status_code=404, detail="处方不存在")
    h_result = await db.execute(
        select(PrescriptionHerb).where(PrescriptionHerb.prescription_id == rx.id)
    )
    herbs = h_result.scalars().all()
    herb_lines = [f"{h.herb_name} {h.dosage_g}g ({h.dosage_liang}两)" + (f" [{h.processing}]" if h.processing else "") for h in herbs]
    total_cost_estimate = round(len(herbs) * 3.5 * rx.doses, 1)

    return {
        "pharmacy_version": {
            "formula_name": rx.classic_formula_name or "自拟方",
            "herbs": herb_lines,
            "doses": rx.doses,
            "cooking_instructions": rx.cooking_instructions or "水煎服，日一剂，分两次温服",
            "estimated_cost": f"约{total_cost_estimate}元",
        },
        "patient_version": rx.patient_notes or f"请按医嘱服药，共{rx.doses}剂。{rx.cooking_instructions or ''}",
        "internal_version": rx.internal_notes,
    }

@router.get("/classics/", summary="经典方剂列表")
async def list_classic_formulas(search: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    q = select(ClassicFormula)
    if search:
        q = q.where(ClassicFormula.name.contains(search))
    q = q.order_by(ClassicFormula.name)
    result = await db.execute(q)
    formulas = result.scalars().all()
    return [{"id": f.id, "name": f.name, "source": f.source,
             "indication": f.indication, "syndrome": f.syndrome} for f in formulas]

@router.get("/classics/{formula_id}", summary="获取经典方剂详情及药味")
async def get_classic_formula(formula_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ClassicFormula).where(ClassicFormula.id == formula_id))
    formula = result.scalar_one_or_none()
    if not formula:
        raise HTTPException(status_code=404, detail="方剂不存在")
    h_result = await db.execute(
        select(ClassicFormulaHerb).where(ClassicFormulaHerb.formula_id == formula_id)
    )
    herbs = h_result.scalars().all()
    return {
        "id": formula.id, "name": formula.name, "source": formula.source,
        "indication": formula.indication, "syndrome": formula.syndrome,
        "cooking_notes": formula.cooking_notes,
        "herbs": [{"herb_name": h.herb_name, "dosage_liang": h.dosage_liang,
                   "dosage_g": h.dosage_g, "processing": h.processing} for h in herbs],
    }
