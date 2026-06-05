from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Case schemas
class CaseBase(BaseModel):
    title: str
    description: Optional[str] = None
    patient_id: Optional[str] = None
    modality: Optional[str] = None
    body_part: Optional[str] = None
    diagnosis: Optional[str] = None
    teaching_points: Optional[str] = None
    difficulty_level: Optional[int] = 1

class CaseCreate(CaseBase):
    pass

class CaseUpdate(CaseBase):
    pass

class CaseResponse(CaseBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# CaseImage schemas
class CaseImageBase(BaseModel):
    case_id: int
    dicom_instance_id: str
    image_type: Optional[str] = None
    description: Optional[str] = None

class CaseImageCreate(CaseImageBase):
    pass

class CaseImageResponse(CaseImageBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Statistics schema
class Statistics(BaseModel):
    total_cases: int
    total_images: int
    available_modalities: List[str]

# Health check schema
class HealthCheck(BaseModel):
    status: str
    message: str
