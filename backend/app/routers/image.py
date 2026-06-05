from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models import CaseImage
from ..schemas import CaseImageCreate, CaseImageResponse

router = APIRouter(prefix="/case-images", tags=["case-images"])

@router.post("/", response_model=CaseImageResponse)
async def create_case_image(image: CaseImageCreate, db: Session = Depends(get_db)):
    """添加病例影像"""
    db_image = CaseImage(**image.dict())
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image

@router.get("/", response_model=List[CaseImageResponse])
async def read_case_images(
    case_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """获取影像列表"""
    query = db.query(CaseImage)

    if case_id:
        query = query.filter(CaseImage.case_id == case_id)

    images = query.offset(skip).limit(limit).all()
    return images

@router.get("/{image_id}", response_model=CaseImageResponse)
async def read_case_image(image_id: int, db: Session = Depends(get_db)):
    """获取单个影像"""
    image = db.query(CaseImage).filter(CaseImage.id == image_id).first()
    if image is None:
        raise HTTPException(status_code=404, detail="影像未找到")
    return image

@router.delete("/{image_id}")
async def delete_case_image(image_id: int, db: Session = Depends(get_db)):
    """删除影像"""
    image = db.query(CaseImage).filter(CaseImage.id == image_id).first()
    if image is None:
        raise HTTPException(status_code=404, detail="影像未找到")

    db.delete(image)
    db.commit()
    return {"message": "影像已删除"}
