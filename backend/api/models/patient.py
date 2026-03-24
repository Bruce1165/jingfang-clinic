import uuid
import enum
from sqlalchemy import Column, String, Integer, Date, DateTime, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base

class GenderEnum(str, enum.Enum):
    male = "male"
    female = "female"
    other = "other"

class Patient(Base):
    __tablename__ = "patients"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(50), nullable=False, index=True)
    gender = Column(Enum(GenderEnum), nullable=False)
    birth_date = Column(Date, nullable=True)
    age = Column(Integer, nullable=True)
    phone = Column(String(20), nullable=True)
    address = Column(Text, nullable=True)

    # 生辰八字
    bazi_year = Column(String(10), nullable=True)
    bazi_month = Column(String(10), nullable=True)
    bazi_day = Column(String(10), nullable=True)
    bazi_hour = Column(String(10), nullable=True)
    birth_hour_raw = Column(String(10), nullable=True)
    wuxing_distribution = Column(Text, nullable=True)  # JSON字符串
    constitution_hint = Column(Text, nullable=True)

    notes = Column(Text, nullable=True)
    is_active = Column(Integer, default=1)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    visits = relationship("Visit", back_populates="patient",
                         order_by="Visit.visit_date.desc()")
