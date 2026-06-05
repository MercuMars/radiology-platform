from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Case, CaseImage
from ..schemas import Statistics

router = APIRouter(prefix="/stats", tags=["statistics"])

@router.get("/", response_model=Statistics)
async def get_statistics(db: Session = Depends(get_db)):
    """获取平台统计数据"""
    total_cases = db.query(Case).count()
    total_images = db.query(CaseImage).count()
    modalities = db.query(Case.modality).distinct().all()

    return {
        "total_cases": total_cases,
        "total_images": total_images,
        "available_modalities": [m[0] for m in modalities if m[0]]
    }
