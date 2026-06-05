from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models import Case
from ..schemas import CaseCreate, CaseUpdate, CaseResponse

router = APIRouter(prefix="/cases", tags=["cases"])

@router.post("/", response_model=CaseResponse)
async def create_case(case: CaseCreate, db: Session = Depends(get_db)):
    """创建新病例"""
    db_case = Case(**case.dict())
    db.add(db_case)
    db.commit()
    db.refresh(db_case)
    return db_case

@router.get("/", response_model=List[CaseResponse])
async def read_cases(
    skip: int = 0,
    limit: int = 100,
    modality: Optional[str] = None,
    body_part: Optional[str] = None,
    difficulty_level: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """获取病例列表"""
    query = db.query(Case)

    # 应用过滤条件
    if modality:
        query = query.filter(Case.modality == modality)
    if body_part:
        query = query.filter(Case.body_part == body_part)
    if difficulty_level:
        query = query.filter(Case.difficulty_level == difficulty_level)

    cases = query.offset(skip).limit(limit).all()
    return cases

@router.get("/{case_id}", response_model=CaseResponse)
async def read_case(case_id: int, db: Session = Depends(get_db)):
    """获取单个病例"""
    case = db.query(Case).filter(Case.id == case_id).first()
    if case is None:
        raise HTTPException(status_code=404, detail="病例未找到")
    return case

@router.put("/{case_id}", response_model=CaseResponse)
async def update_case(case_id: int, case: CaseUpdate, db: Session = Depends(get_db)):
    """更新病例"""
    db_case = db.query(Case).filter(Case.id == case_id).first()
    if db_case is None:
        raise HTTPException(status_code=404, detail="病例未找到")

    for key, value in case.dict(exclude_unset=True).items():
        setattr(db_case, key, value)

    db.commit()
    db.refresh(db_case)
    return db_case

@router.delete("/{case_id}")
async def delete_case(case_id: int, db: Session = Depends(get_db)):
    """删除病例"""
    case = db.query(Case).filter(Case.id == case_id).first()
    if case is None:
        raise HTTPException(status_code=404, detail="病例未找到")

    db.delete(case)
    db.commit()
    return {"message": "病例已删除"}
