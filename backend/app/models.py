from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Case(Base):
    __tablename__ = "cases"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    patient_id = Column(String(100))
    modality = Column(String(50))  # CT, MRI, X-Ray, etc.
    body_part = Column(String(100))
    diagnosis = Column(Text)
    teaching_points = Column(Text)
    difficulty_level = Column(Integer, default=1)  # 1-5
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    images = relationship("CaseImage", back_populates="case", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Case(id={self.id}, title='{self.title}')>"

class CaseImage(Base):
    __tablename__ = "case_images"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.id", ondelete="CASCADE"))
    dicom_instance_id = Column(String(255))  # Orthanc instance ID
    image_type = Column(String(50))  # axial, sagittal, coronal, etc.
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    case = relationship("Case", back_populates="images")

    def __repr__(self):
        return f"<CaseImage(id={self.id}, case_id={self.case_id})>"
