"""
PostgreSQL 데이터베이스 설정
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# 데이터베이스 URL 설정
# PostgreSQL 사용 시: postgresql://postgres:postgres@localhost:5432/template_management
# SQLite 사용 시 (PostgreSQL 미설치): sqlite:///./template_management.db
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./template_management.db"
)

# SQLAlchemy 엔진 생성
engine = create_engine(DATABASE_URL)

# 세션 로컬 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base 클래스
Base = declarative_base()


def get_db():
    """데이터베이스 세션 의존성"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """데이터베이스 초기화"""
    Base.metadata.create_all(bind=engine)
