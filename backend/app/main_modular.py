from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import case_router, image_router, stats_router

# Create database tables
Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI(
    title="放射科专业病例阅片学习平台 API",
    description="A radiology case study learning platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(case_router, prefix="/api")
app.include_router(image_router, prefix="/api")
app.include_router(stats_router, prefix="/api")

# Health check
@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "message": "放射科专业病例阅片学习平台 API 运行正常"}

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "欢迎使用放射科专业病例阅片学习平台 API",
        "docs": "/docs",
        "health": "/api/health"
    }
