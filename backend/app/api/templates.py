from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
import os
import uuid
import shutil
import logging
from datetime import datetime

router = APIRouter()
logger = logging.getLogger(__name__)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 메모리에 템플릿 저장 (추후 DB로 전환)
templates_db = {}


@router.post("/upload")
async def upload_template(
    file: UploadFile = File(...)
):
    """
    템플릿 파일 업로드
    - 워드(.doc, .docx) 파일 업로드
    - 파일 이름을 템플릿 이름으로 자동 사용
    - 분석 없이 바로 변환 가능
    """
    try:
        logger.info(f"템플릿 업로드 요청 - filename: {file.filename}")

        # 파일 확장자 검증
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in ['.docx', '.doc']:
            logger.warning(f"지원하지 않는 파일 형식 - filename: {file.filename}, ext: {file_ext}")
            raise HTTPException(
                status_code=400,
                detail="지원하지 않는 파일 형식입니다. .doc 또는 .docx 파일만 업로드 가능합니다."
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
            "status": "ready",
            "created_at": datetime.now().isoformat()
        }

        templates_db[template_id] = template_info
        logger.info(f"템플릿 정보 저장 완료 - template_id: {template_id}")

        return {
            "success": True,
            "data": {
                "template_id": template_id,
                "name": template_info["name"],
                "status": "ready",
                "message": "파일이 성공적으로 업로드되었습니다. HWP로 변환할 수 있습니다."
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
            "created_at": template["created_at"]
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
