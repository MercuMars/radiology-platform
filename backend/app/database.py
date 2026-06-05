from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import time

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://radio:radio123@db/cases")

# Create engine with retry logic for container startup race conditions
def create_engine_with_retry(url, max_retries=30, retry_delay=2):
    """Create SQLAlchemy engine, retrying on connection failure (for Docker startup ordering)."""
    last_exception = None
    for attempt in range(1, max_retries + 1):
        try:
            engine = create_engine(
                url,
                pool_pre_ping=True,
                pool_size=10,
                max_overflow=20
            )
            # Test the connection
            with engine.connect():
                pass
            print(f"[DB] Connected successfully on attempt {attempt}")
            return engine
        except Exception as e:
            last_exception = e
            print(f"[DB] Connection attempt {attempt}/{max_retries} failed: {e}")
            if attempt < max_retries:
                print(f"[DB] Retrying in {retry_delay}s...")
                time.sleep(retry_delay)

    raise RuntimeError(f"[DB] Failed to connect after {max_retries} attempts: {last_exception}")

engine = create_engine_with_retry(DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
