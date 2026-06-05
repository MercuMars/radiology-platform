from fastapi import FastAPI, HTTPException, Depends, status, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
import hashlib
import jwt
import os
import httpx

from .database import engine, SessionLocal, Base
from .models import User, System, Case, CaseImage, Comment, Report, Collection, Template, Annotation

# Database configuration
SECRET_KEY = os.getenv("SECRET_KEY", "super_secret_medical_key_2024")
ALGORITHM = "HS256"

def hash_password(password: str) -> str:
    """使用 SHA256 哈希密码"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return hash_password(plain_password) == hashed_password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# ==================== Pydantic Models ====================

class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    role: str
    class Config:
        from_attributes = True

class SystemCreate(BaseModel):
    name: str
    code: str
    description: Optional[str] = None
    icon: Optional[str] = None
    sort_order: Optional[int] = 0

class SystemResponse(BaseModel):
    id: int
    name: str
    code: str
    description: Optional[str] = None
    icon: Optional[str] = None
    sort_order: int
    class Config:
        from_attributes = True

class CaseCreate(BaseModel):
    title: str
    description: Optional[str] = None
    patient_id: Optional[str] = None
    modality: Optional[str] = None
    system_id: Optional[int] = None
    body_part: Optional[str] = None
    diagnosis: Optional[str] = None
    teaching_points: Optional[str] = None
    difficulty_level: Optional[int] = 1

class CaseResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    patient_id: Optional[str] = None
    modality: Optional[str] = None
    system_id: Optional[int] = None
    body_part: Optional[str] = None
    diagnosis: Optional[str] = None
    teaching_points: Optional[str] = None
    difficulty_level: Optional[int] = 1
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

class CaseImageCreate(BaseModel):
    case_id: int
    dicom_instance_id: str
    image_type: Optional[str] = None
    description: Optional[str] = None

class CaseImageResponse(BaseModel):
    id: int
    case_id: int
    dicom_instance_id: str
    image_type: Optional[str] = None
    description: Optional[str] = None
    created_at: datetime
    class Config:
        from_attributes = True

class CommentCreate(BaseModel):
    content: str

class CommentResponse(BaseModel):
    id: int
    case_id: int
    user_id: int
    username: Optional[str] = None
    content: str
    created_at: datetime
    class Config:
        from_attributes = True

class ReportCreate(BaseModel):
    case_id: int
    technique: Optional[str] = None
    findings: Optional[str] = None
    impression: Optional[str] = None

class ReportResponse(BaseModel):
    id: int
    case_id: int
    technique: Optional[str] = None
    findings: Optional[str] = None
    impression: Optional[str] = None
    created_by: Optional[int] = None
    created_at: datetime
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class AnnotationCreate(BaseModel):
    annotation_data: str

# ==================== FastAPI App ====================

app = FastAPI(
    title="放射科专业病例阅片学习平台 API",
    description="支持图谱分类、结构化模板与标注持久化",
    version="1.1.0",
    root_path="/api"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="无效的认证凭证")
        user = db.query(User).filter(User.username == username).first()
        if user is None:
            raise HTTPException(status_code=401, detail="用户不存在")
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="登录已过期，请重新登录")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="无效的认证凭证")

@app.on_event("startup")
async def startup():
    Base.metadata.create_all(bind=engine)
    # 初始化默认系统分类（按放射科亚专业分组）
    db = SessionLocal()
    try:
        if db.query(System).count() == 0:
            default_systems = [
                System(name="神经/头颈影像", code="neuro_head_neck", description="🧠 脑、脊髓、五官、颈部（眼、耳、鼻、喉、甲状腺、淋巴结）", icon="🧠", sort_order=1),
                System(name="心胸影像", code="cardiothoracic", description="❤️ 肺、心脏、大血管、乳腺", icon="❤️", sort_order=2),
                System(name="腹盆部影像", code="abdominopelvic", description="🫀 肝胆胰脾、胃肠、泌尿生殖系统", icon="🫀", sort_order=3),
                System(name="骨肌影像", code="musculoskeletal", description="🦴 骨骼、关节、肌肉、韧带", icon="🦴", sort_order=4),
                System(name="其他", code="other", description="📋 其他未分类影像", icon="📋", sort_order=5),
            ]
            db.add_all(default_systems)
            db.commit()

        # 初始化默认报告模板
        if db.query(Template).count() == 0:
            default_templates = [
                Template(name="LI-RADS 肝脏结节报告", modality="CT", body_part="肝脏", content_findings="肝脏形态大小正常，表面光滑。动脉期可见一大小约[]mm强化结节，静脉期/延迟期呈廓清表现，包膜强化(+)。", content_impression="符合 LI-RADS 5类典型肝细胞癌表现。"),
                Template(name="肺结节标准报告 (Lung-RADS)", modality="CT", body_part="肺部", content_findings="双肺纹理清晰。[]肺[]叶可见一实性/磨玻璃结节，直径约[]mm，边缘见分叶/毛刺/胸膜牵拉征。", content_impression="肺部结节，建议结合临床及历史影像对比，Lung-RADS []类。")
            ]
            db.add_all(default_templates)
            db.commit()
    finally:
        db.close()

# ==================== Health Check ====================

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "放射科专业病例阅片学习平台 API 运行正常"}

# ==================== Auth Endpoints ====================

@app.post("/auth/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="用户名已存在")
    hashed_password = hash_password(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/auth/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    access_token = jwt.encode(
        {"sub": user.username, "user_id": user.id, "exp": datetime.utcnow() + timedelta(days=7)},
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/auth/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

# ==================== System Endpoints ====================

@app.get("/systems/", response_model=List[SystemResponse])
def read_systems(db: Session = Depends(get_db)):
    systems = db.query(System).order_by(System.sort_order).all()
    return systems

@app.post("/systems/", response_model=SystemResponse)
def create_system(system: SystemCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role not in ["teacher", "admin"]:
        raise HTTPException(status_code=403, detail="权限不足")
    db_system = System(**system.dict())
    db.add(db_system)
    db.commit()
    db.refresh(db_system)
    return db_system

# ==================== Case Endpoints ====================

@app.post("/cases/", response_model=CaseResponse)
def create_case(case: CaseCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role not in ["teacher", "admin"]:
        raise HTTPException(status_code=403, detail="权限不足，只有教师可以创建病例")
    db_case = Case(**case.dict())
    db.add(db_case)
    db.commit()
    db.refresh(db_case)
    return db_case

@app.get("/cases/", response_model=List[CaseResponse])
def read_cases(
    skip: int = 0,
    limit: int = 100,
    system_id: Optional[int] = None,
    modality: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Case)
    if system_id:
        query = query.filter(Case.system_id == system_id)
    if modality:
        query = query.filter(Case.modality == modality)
    cases = query.offset(skip).limit(limit).all()
    return cases

@app.get("/cases/{case_id}", response_model=CaseResponse)
def read_case(case_id: int, db: Session = Depends(get_db)):
    case = db.query(Case).filter(Case.id == case_id).first()
    if case is None:
        raise HTTPException(status_code=404, detail="病例未找到")
    return case

@app.put("/cases/{case_id}", response_model=CaseResponse)
def update_case(case_id: int, case: CaseCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role not in ["teacher", "admin"]:
        raise HTTPException(status_code=403, detail="权限不足")
    db_case = db.query(Case).filter(Case.id == case_id).first()
    if db_case is None:
        raise HTTPException(status_code=404, detail="病例未找到")
    for key, value in case.dict().items():
        setattr(db_case, key, value)
    db.commit()
    db.refresh(db_case)
    return db_case

@app.delete("/cases/{case_id}")
def delete_case(case_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role not in ["teacher", "admin"]:
        raise HTTPException(status_code=403, detail="权限不足")
    case = db.query(Case).filter(Case.id == case_id).first()
    if case is None:
        raise HTTPException(status_code=404, detail="病例未找到")
    db.delete(case)
    db.commit()
    return {"message": "病例已删除"}

# ==================== Case Image Endpoints ====================

@app.post("/case-images/", response_model=CaseImageResponse)
def create_case_image(image: CaseImageCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role not in ["teacher", "admin"]:
        raise HTTPException(status_code=403, detail="权限不足")
    db_image = CaseImage(**image.dict())
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image

@app.get("/case-images/", response_model=List[CaseImageResponse])
def read_case_images(case_id: Optional[int] = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    query = db.query(CaseImage)
    if case_id:
        query = query.filter(CaseImage.case_id == case_id)
    images = query.offset(skip).limit(limit).all()
    return images

@app.get("/case-images/{image_id}", response_model=CaseImageResponse)
def read_case_image(image_id: int, db: Session = Depends(get_db)):
    image = db.query(CaseImage).filter(CaseImage.id == image_id).first()
    if image is None:
        raise HTTPException(status_code=404, detail="影像未找到")
    return image

@app.delete("/case-images/{image_id}")
def delete_case_image(image_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role not in ["teacher", "admin"]:
        raise HTTPException(status_code=403, detail="权限不足")
    image = db.query(CaseImage).filter(CaseImage.id == image_id).first()
    if image is None:
        raise HTTPException(status_code=404, detail="影像未找到")
    db.delete(image)
    db.commit()
    return {"message": "影像已删除"}

# ==================== Comment Endpoints ====================

@app.post("/cases/{case_id}/comments", response_model=CommentResponse)
def add_comment(case_id: int, comment: CommentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    case = db.query(Case).filter(Case.id == case_id).first()
    if case is None:
        raise HTTPException(status_code=404, detail="病例未找到")
    db_comment = Comment(case_id=case_id, user_id=current_user.id, content=comment.content)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return CommentResponse(
        id=db_comment.id,
        case_id=db_comment.case_id,
        user_id=db_comment.user_id,
        username=current_user.username,
        content=db_comment.content,
        created_at=db_comment.created_at
    )

@app.get("/cases/{case_id}/comments", response_model=List[CommentResponse])
def read_comments(case_id: int, db: Session = Depends(get_db)):
    comments = db.query(Comment).filter(Comment.case_id == case_id).order_by(Comment.created_at).all()
    result = []
    for c in comments:
        user = db.query(User).filter(User.id == c.user_id).first()
        result.append(CommentResponse(
            id=c.id,
            case_id=c.case_id,
            user_id=c.user_id,
            username=user.username if user else "未知用户",
            content=c.content,
            created_at=c.created_at
        ))
    return result

# ==================== Report Endpoints ====================

@app.post("/cases/{case_id}/reports", response_model=ReportResponse)
def add_report(case_id: int, report: ReportCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role not in ["teacher", "admin"]:
        raise HTTPException(status_code=403, detail="权限不足，只有教师可以添加报告")
    case = db.query(Case).filter(Case.id == case_id).first()
    if case is None:
        raise HTTPException(status_code=404, detail="病例未找到")
    db_report = Report(case_id=case_id, technique=report.technique, findings=report.findings, impression=report.impression, created_by=current_user.id)
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report

@app.get("/cases/{case_id}/reports", response_model=List[ReportResponse])
def read_reports(case_id: int, db: Session = Depends(get_db)):
    reports = db.query(Report).filter(Report.case_id == case_id).order_by(Report.created_at.desc()).all()
    return reports

# ==================== Templates & Annotations ====================

@app.get("/templates/")
def get_templates(db: Session = Depends(get_db)):
    templates = db.query(Template).all()
    return [{"id": t.id, "name": t.name, "findings": t.content_findings, "impression": t.content_impression} for t in templates]

@app.post("/cases/{case_id}/annotations")
def save_annotation(case_id: int, anno: AnnotationCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_anno = Annotation(case_id=case_id, user_id=current_user.id, annotation_data=anno.annotation_data)
    db.add(db_anno)
    db.commit()
    return {"status": "success", "msg": "标注数据已保存"}

@app.get("/cases/{case_id}/annotations")
def get_annotations(case_id: int, db: Session = Depends(get_db)):
    annos = db.query(Annotation).filter(Annotation.case_id == case_id).order_by(Annotation.created_at.desc()).all()
    res = []
    for a in annos:
        user = db.query(User).filter(User.id == a.user_id).first()
        res.append({
            "id": a.id, "username": user.username if user else "未知",
            "data": a.annotation_data, "time": a.created_at
        })
    return res

# ==================== DICOM Upload Endpoints ====================

ORTHANC_URL = os.getenv("ORTHANC_URL", "http://orthanc:8042")

@app.post("/dicom/upload")
async def upload_dicom_files(
    files: List[UploadFile] = File(...),
    current_user: User = Depends(get_current_user)
):
    """上传 DICOM 文件到 Orthanc"""
    if current_user.role not in ["teacher", "admin"]:
        raise HTTPException(status_code=403, detail="权限不足，只有教师可以上传 DICOM 文件")

    results = []
    async with httpx.AsyncClient() as client:
        for file in files:
            if not file.filename.endswith('.dcm'):
                results.append({"filename": file.filename, "status": "skipped", "reason": "不是 DICOM 文件"})
                continue

            try:
                content = await file.read()
                response = await client.post(
                    f"{ORTHANC_URL}/instances",
                    content=content,
                    headers={"Content-Type": "application/dicom"},
                    timeout=30.0
                )
                if response.status_code == 200:
                    result = response.json()
                    results.append({
                        "filename": file.filename,
                        "status": "success",
                        "instance_id": result.get("ID"),
                        "patient_id": result.get("PatientID"),
                        "study_id": result.get("ParentStudy"),
                        "series_id": result.get("ParentSeries")
                    })
                else:
                    results.append({"filename": file.filename, "status": "error", "reason": response.text})
            except Exception as e:
                results.append({"filename": file.filename, "status": "error", "reason": str(e)})

    return {"uploaded": len([r for r in results if r["status"] == "success"]), "results": results}

@app.post("/dicom/upload-folder")
async def upload_dicom_folder(
    files: List[UploadFile] = File(...),
    case_id: Optional[int] = None,
    current_user: User = Depends(get_current_user)
):
    """上传 DICOM 文件夹（多个文件）到 Orthanc，并关联到病例"""
    if current_user.role not in ["teacher", "admin"]:
        raise HTTPException(status_code=403, detail="权限不足")

    results = []
    uploaded_instances = []

    async with httpx.AsyncClient() as client:
        for file in files:
            try:
                content = await file.read()
                response = await client.post(
                    f"{ORTHANC_URL}/instances",
                    content=content,
                    headers={"Content-Type": "application/dicom"},
                    timeout=30.0
                )
                if response.status_code == 200:
                    result = response.json()
                    instance_id = result.get("ID")
                    uploaded_instances.append(instance_id)
                    results.append({
                        "filename": file.filename,
                        "status": "success",
                        "instance_id": instance_id
                    })

                    # 如果指定了 case_id，保存关联
                    if case_id and instance_id:
                        db_image = CaseImage(
                            case_id=case_id,
                            dicom_instance_id=instance_id,
                            image_type="axial",
                            description=f"从 {file.filename} 上传"
                        )
                        db = SessionLocal()
                        try:
                            db.add(db_image)
                            db.commit()
                        finally:
                            db.close()
                else:
                    results.append({"filename": file.filename, "status": "error", "reason": response.text})
            except Exception as e:
                results.append({"filename": file.filename, "status": "error", "reason": str(e)})

    return {
        "uploaded": len(uploaded_instances),
        "instance_ids": uploaded_instances,
        "results": results
    }

@app.get("/dicom/studies")
async def list_dicom_studies(current_user: User = Depends(get_current_user)):
    """列出 Orthanc 中的所有研究"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{ORTHANC_URL}/studies", timeout=10.0)
            if response.status_code == 200:
                studies = response.json()
                study_list = []
                for study_id in studies:
                    detail_response = await client.get(f"{ORTHANC_URL}/studies/{study_id}", timeout=10.0)
                    if detail_response.status_code == 200:
                        detail = detail_response.json()
                        # Orthanc 嵌套结构：MainDicomTags 和 PatientMainDicomTags
                        main_tags = detail.get("MainDicomTags", {})
                        patient_tags = detail.get("PatientMainDicomTags", {})
                        study_list.append({
                            "orthanc_id": study_id,
                            "study_instance_uid": main_tags.get("StudyInstanceUID", ""),
                            "patient_name": patient_tags.get("PatientName", "未知"),
                            "patient_id": patient_tags.get("PatientID", "未知"),
                            "study_date": main_tags.get("StudyDate", ""),
                            "study_description": main_tags.get("StudyDescription", ""),
                            "modality": main_tags.get("ModalitiesInStudy", [])
                        })
                return study_list
            return []
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"无法连接 Orthanc: {str(e)}")

@app.get("/dicom/studies/{study_id}")
async def get_dicom_study(study_id: str, current_user: User = Depends(get_current_user)):
    """获取 Orthanc 中特定研究的详情"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{ORTHANC_URL}/studies/{study_id}", timeout=10.0)
            if response.status_code == 200:
                return response.json()
            raise HTTPException(status_code=404, detail="研究未找到")
        except httpx.RequestError:
            raise HTTPException(status_code=500, detail="无法连接 Orthanc")

@app.delete("/dicom/studies/{study_id}")
async def delete_dicom_study(study_id: str, current_user: User = Depends(get_current_user)):
    """删除 Orthanc 中的研究"""
    if current_user.role not in ["admin"]:
        raise HTTPException(status_code=403, detail="权限不足")

    async with httpx.AsyncClient() as client:
        try:
            response = await client.delete(f"{ORTHANC_URL}/studies/{study_id}", timeout=10.0)
            if response.status_code == 200:
                return {"message": "研究已删除"}
            raise HTTPException(status_code=404, detail="研究未找到")
        except httpx.RequestError:
            raise HTTPException(status_code=500, detail="无法连接 Orthanc")

# ==================== Statistics ====================

@app.get("/stats/")
def get_statistics(db: Session = Depends(get_db)):
    total_cases = db.query(Case).count()
    total_images = db.query(CaseImage).count()
    total_users = db.query(User).count()
    modalities = db.query(Case.modality).distinct().all()
    systems = db.query(System).all()
    system_stats = []
    for s in systems:
        case_count = db.query(Case).filter(Case.system_id == s.id).count()
        system_stats.append({"system": s.name, "code": s.code, "case_count": case_count})
    return {
        "total_cases": total_cases,
        "total_images": total_images,
        "total_users": total_users,
        "available_modalities": [m[0] for m in modalities if m[0]],
        "system_stats": system_stats
    }
