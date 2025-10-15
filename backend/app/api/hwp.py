from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Dict, Any
import os
import logging
from app.api.templates import templates_db
from app.services.hwp_generator import HwpGenerator

router = APIRouter()
logger = logging.getLogger(__name__)

# HWP 생성기
hwp_generator = HwpGenerator()

class HwpGenerateRequest(BaseModel):
    template_id: str
    filename: str

@router.post("/generate")
async def generate_hwp(request: HwpGenerateRequest):
    """
    HWP 파일 생성
    - 템플릿 ID를 받아 HWP 파일 생성
    - 파일명을 지정하지 않으면 템플릿 이름 사용
    """
    try:
        logger.info(f"HWP 생성 요청 - template_id: {request.template_id}, filename: {request.filename}")

        # 템플릿 확인
        if request.template_id not in templates_db:
            logger.error(f"템플릿을 찾을 수 없음 - template_id: {request.template_id}")
            logger.error(f"현재 템플릿 DB: {list(templates_db.keys())}")
            raise HTTPException(status_code=404, detail="템플릿을 찾을 수 없습니다.")

        template = templates_db[request.template_id]
        logger.info(f"템플릿 찾음 - name: {template.get('name')}, status: {template.get('status')}")

        # HWP 생성
        logger.info("HWP 생성 시작...")
        result = await hwp_generator.generate_hwp(
            template=template,
            filename=request.filename
        )

        if not result["success"]:
            logger.error(f"HWP 생성 실패 - {result['message']}")
            raise HTTPException(status_code=500, detail=result["message"])

        logger.info(f"HWP 생성 성공 - filename: {result['filename']}")

        # 파일이 생성되었다면 다운로드 URL 반환
        if os.path.exists(result["file_path"]):
            logger.info(f"HWP 파일 존재 확인 - path: {result['file_path']}")
            return {
                "success": True,
                "filename": result["filename"],
                "file_url": f"/api/hwp/download/{result['filename']}",
                "message": result["message"]
            }

        logger.warning("HWP 파일이 생성되었으나 파일을 찾을 수 없음")
        return {
            "success": True,
            "message": result["message"]
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"HWP 생성 중 예외 발생: {str(e)}")
        raise HTTPException(status_code=500, detail=f"HWP 생성 중 오류 발생: {str(e)}")


@router.get("/download/{filename}")
async def download_hwp(filename: str):
    """HWP 파일 다운로드"""
    file_path = os.path.join("outputs", filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="파일을 찾을 수 없습니다.")

    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/octet-stream"
    )
