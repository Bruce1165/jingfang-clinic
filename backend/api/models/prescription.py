import uuid
from sqlalchemy import Column, String, Integer, Float, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base

class Prescription(Base):
    __tablename__ = "prescriptions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    visit_id = Column(String(36), ForeignKey("visits.id"), nullable=False, index=True)
    classic_formula_name = Column(String(100), nullable=True)   # 基础方名
    modification_notes = Column(Text, nullable=True)            # 加减说明
    cooking_instructions = Column(Text, nullable=True)          # 煎服法
    doses = Column(Integer, default=7)                          # 剂数
    internal_notes = Column(Text, nullable=True)                # 内部备注
    patient_notes = Column(Text, nullable=True)                 # 给患者的说明
    created_at = Column(DateTime, server_default=func.now())

    visit = relationship("Visit", back_populates="prescriptions")
    herbs = relationship("PrescriptionHerb", back_populates="prescription",
                        cascade="all, delete-orphan")

class PrescriptionHerb(Base):
    __tablename__ = "prescription_herbs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    prescription_id = Column(String(36), ForeignKey("prescriptions.id"), nullable=False)
    herb_name = Column(String(50), nullable=False)
    dosage_g = Column(Float, nullable=False)          # 克
    dosage_liang = Column(Float, nullable=True)       # 两（自动换算）
    processing = Column(String(50), nullable=True)    # 炮制：生用/炮/先煎/包煎等
    notes = Column(String(200), nullable=True)

    prescription = relationship("Prescription", back_populates="herbs")

class ClassicFormula(Base):
    __tablename__ = "classic_formulas"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False, unique=True, index=True)
    source = Column(String(100), nullable=True)       # 来源：伤寒论/金匮要略等
    indication = Column(Text, nullable=True)          # 主治
    syndrome = Column(String(200), nullable=True)     # 适应证候
    cooking_notes = Column(Text, nullable=True)       # 经典煎法
    notes = Column(Text, nullable=True)

    herbs = relationship("ClassicFormulaHerb", back_populates="formula",
                        cascade="all, delete-orphan")

class ClassicFormulaHerb(Base):
    __tablename__ = "classic_formula_herbs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    formula_id = Column(String(36), ForeignKey("classic_formulas.id"), nullable=False)
    herb_name = Column(String(50), nullable=False)
    dosage_liang = Column(Float, nullable=True)       # 原典用量（两）
    dosage_g = Column(Float, nullable=True)           # 现代克数
    processing = Column(String(50), nullable=True)
    notes = Column(String(200), nullable=True)

    formula = relationship("ClassicFormula", back_populates="herbs")
