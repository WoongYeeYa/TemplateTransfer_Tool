from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.api import templates, hwp
from app.core.logging_config import logger
import os

# 로그 디렉토리 생성
os.makedirs("logs", exist_ok=True)

app = FastAPI(
    title="Template Management API",
    description="워드/한글 파일 양식 자동화 시스템",
    version="1.0.0"
)

logger.info("=" * 50)
logger.info("Template Management API Starting...")
logger.info("=" * 50)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Validation 에러 핸들러
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    body = await request.body()
    logger.error(f"Validation error on {request.method} {request.url}")
    logger.error(f"Request body: {body.decode('utf-8')}")
    logger.error(f"Validation errors: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": exc.errors(),
            "body": body.decode('utf-8')
        }
    )

# 라우터 등록
app.include_router(templates.router, prefix="/api/templates", tags=["templates"])
app.include_router(hwp.router, prefix="/api/hwp", tags=["hwp"])

@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {
        "message": "Template Management API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
