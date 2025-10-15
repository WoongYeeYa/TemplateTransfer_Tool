from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from typing import List
import os
import uuid
import shutil
import logging
from datetime import datetime
from app.services.document_analyzer import DocumentAnalyzer

router = APIRouter()
logger = logging.getLogger(__name__)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 메모리에 템플릿 저장 (추후 DB로 전환)
templates_db = {}

# 문서 분석 서비스
analyzer = DocumentAnalyzer()

async def analyze_template_background(template_id: str, file_path: str, file_type: str):
    """백그라운드에서 템플릿 분석 수행"""
    try:
        logger.info(f"템플릿 분석 시작 - template_id: {template_id}, file_type: {file_type}")

        # 상태 업데이트
        if template_id in templates_db:
            templates_db[template_id]["status"] = "analyzing"

        # 문서 분석
        analysis_result = await analyzer.analyze_document(file_path, file_type)
        logger.info(f"템플릿 분석 완료 - template_id: {template_id}")

        # 결과 저장
        if template_id in templates_db:
            templates_db[template_id]["analysis_result"] = analysis_result
            templates_db[template_id]["status"] = "analyzed"

    except Exception as e:
        logger.exception(f"템플릿 분석 실패 - template_id: {template_id}, error: {str(e)}")
        if template_id in templates_db:
            templates_db[template_id]["status"] = "analysis_failed"
            templates_db[template_id]["error"] = str(e)


@router.post("/upload")
async def upload_template(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    """
    템플릿 파일 업로드
    - 워드(.docx) 또는 한글(.hwp) 파일 업로드
    - 파일 이름을 템플릿 이름으로 자동 사용
    - 자동으로 분석 시작
    """
    try:
        logger.info(f"템플릿 업로드 요청 - filename: {file.filename}")

        # 파일 확장자 검증
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in ['.docx', '.hwp', '.doc']:
            logger.warning(f"지원하지 않는 파일 형식 - filename: {file.filename}, ext: {file_ext}")
            raise HTTPException(
                status_code=400,
                detail="지원하지 않는 파일 형식입니다. .docx 또는 .hwp 파일만 업로드 가능합니다."
            )

        # 고유 ID 생성
        template_id = str(uuid.uuid4())
        logger.info(f"템플릿 ID 생성 - template_id: {template_id}")

        # 파일 저장
        file_path = os.path.join(UPLOAD_DIR, f"{template_id}{file_ext}")

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        logger.info(f"파일 저장 완료 - path: {file_path}")

        # 템플릿 정보 저장 (파일 이름을 템플릿 이름으로 사용)
        template_info = {
            "id": template_id,
            "name": file.filename,
            "description": "",
            "original_filename": file.filename,
            "file_path": file_path,
            "file_type": file_ext,
            "status": "uploaded",
            "created_at": datetime.now().isoformat(),
            "analysis_result": None
        }

        templates_db[template_id] = template_info
        logger.info(f"템플릿 정보 저장 완료 - template_id: {template_id}")

        # 백그라운드에서 문서 분석 시작
        background_tasks.add_task(analyze_template_background, template_id, file_path, file_ext)
        logger.info(f"백그라운드 분석 작업 추가 - template_id: {template_id}")

        return {
            "success": True,
            "data": {
                "template_id": template_id,
                "name": template_info["name"],
                "status": "uploaded",
                "message": "파일이 성공적으로 업로드되었습니다. 분석이 시작됩니다."
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"템플릿 업로드 중 예외 발생: {str(e)}")
        raise HTTPException(status_code=500, detail=f"파일 업로드 중 오류 발생: {str(e)}")

@router.get("/")
async def list_templates():
    """템플릿 목록 조회"""
    templates_list = [
        {
            "id": template["id"],
            "name": template["name"],
            "description": template["description"],
            "status": template["status"],
            "created_at": template["created_at"],
            "has_analysis": template.get("analysis_result") is not None
        }
        for template in templates_db.values()
    ]

    return {
        "success": True,
        "data": templates_list
    }

@router.get("/{template_id}")
async def get_template(template_id: str):
    """템플릿 상세 조회"""
    if template_id not in templates_db:
        raise HTTPException(status_code=404, detail="템플릿을 찾을 수 없습니다.")

    return {
        "success": True,
        "data": templates_db[template_id]
    }

@router.delete("/{template_id}")
async def delete_template(template_id: str):
    """템플릿 삭제"""
    if template_id not in templates_db:
        raise HTTPException(status_code=404, detail="템플릿을 찾을 수 없습니다.")

    # 파일 삭제
    template = templates_db[template_id]
    if os.path.exists(template["file_path"]):
        os.remove(template["file_path"])

    # DB에서 삭제
    del templates_db[template_id]

    return {
        "success": True,
        "message": "템플릿이 삭제되었습니다."
    }
