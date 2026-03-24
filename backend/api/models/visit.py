import uuid
import enum
from sqlalchemy import Column, String, Integer, DateTime, Text, Enum, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base

class EfficacyEnum(str, enum.Enum):
    improved = "improved"
    unchanged = "unchanged"
    worsened = "worsened"
    first_visit = "first_visit"

class Visit(Base):
    __tablename__ = "visits"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = Column(String(36), ForeignKey("patients.id"), nullable=False, index=True)
    visit_number = Column(Integer, nullable=False, default=1)
    visit_date = Column(DateTime, server_default=func.now())

    # 舌诊
    tongue_color = Column(String(30), nullable=True)
    tongue_coating = Column(String(30), nullable=True)
    tongue_coating_texture = Column(String(30), nullable=True)
    tongue_shape = Column(String(50), nullable=True)

    # 脉象（JSON文本）
    pulse_data = Column(Text, nullable=True)

    # 症状（JSON文本）
    symptoms_structured = Column(Text, nullable=True)

    # 辨证
    syndrome_cold_heat = Column(String(20), nullable=True)
    syndrome_xu_shi = Column(String(20), nullable=True)
    six_channel = Column(String(50), nullable=True)

    # 文字记录
    chief_complaint = Column(Text, nullable=True)
    present_illness = Column(Text, nullable=True)
    inquiry_notes = Column(Text, nullable=True)
    doctor_notes = Column(Text, nullable=True)

    # 疗效
    efficacy = Column(Enum(EfficacyEnum), default=EfficacyEnum.first_visit)
    efficacy_notes = Column(Text, nullable=True)

    # 复诊
    next_visit_date = Column(Date, nullable=True)
    days_of_medicine = Column(Integer, nullable=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    patient = relationship("Patient", back_populates="visits")
    prescriptions = relationship("Prescription", back_populates="visit")
