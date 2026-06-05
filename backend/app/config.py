import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    database_url: str = os.getenv("DATABASE_URL", "postgresql://radio:radio123@db/cases")

    # API
    api_title: str = "放射科专业病例阅片学习平台 API"
    api_description: str = "A radiology case study learning platform"
    api_version: str = "1.0.0"

    # Orthanc
    orthanc_url: str = os.getenv("ORTHANC_URL", "http://orthanc:8042")

    # Security
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
