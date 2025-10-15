"""
DOC/DOCX → HWP 변환 서비스
한글 COM API를 사용하여 Word 파일을 직접 HWP로 변환
"""
import os
import logging
import time
from typing import Dict, Any
import win32com.client
import pythoncom

logger = logging.getLogger(__name__)


class DocToHwpConverter:
    """DOC/DOCX를 HWP로 변환하는 서비스"""

    def __init__(self):
        self.output_dir = "outputs"
        os.makedirs(self.output_dir, exist_ok=True)
        self.hwp = None

    def _initialize_hwp(self):
        """한글 애플리케이션 초기화"""
        try:
            pythoncom.CoInitialize()
            self.hwp = win32com.client.gencache.EnsureDispatch("HWPFrame.HwpObject")
            self.hwp.RegisterModule("FilePathCheckDLL", "FilePathCheckerModule")

            # 보안 경고 완전 비활성화
            # 0x10000000: 모든 보안 경고와 메시지 박스 무시
            self.hwp.SetMessageBoxMode(0x10000000)

            # 한글 창 숨기기 (비가시 모드)
            self.hwp.XHwpWindows.Item(0).Visible = False

            logger.info("한글 COM 초기화 완료 (비가시 모드, 보안 경고 완전 비활성화)")
            return True
        except Exception as e:
            logger.error(f"한글 COM 초기화 실패: {e}")
            return False

    def _close_hwp(self):
        """한글 애플리케이션 종료"""
        try:
            if self.hwp:
                self.hwp.Quit()
                self.hwp = None
            pythoncom.CoUninitialize()
            logger.info("한글 COM 종료 완료")
        except Exception as e:
            logger.error(f"한글 COM 종료 실패: {e}")

    async def convert_to_hwp(
        self,
        source_file_path: str,
        output_filename: str
    ) -> Dict[str, Any]:
        """
        Word 파일을 HWP로 변환

        Args:
            source_file_path: 원본 Word 파일 경로 (.doc, .docx)
            output_filename: 출력 파일 이름 (확장자 제외)

        Returns:
            변환 결과 딕셔너리
        """
        try:
            # 한글 초기화
            if not self._initialize_hwp():
                return {
                    "success": False,
                    "message": "한글 프로그램을 시작할 수 없습니다. 한글이 설치되어 있는지 확인하세요."
                }

            # 원본 파일 경로를 절대 경로로 변환
            abs_source_path = os.path.abspath(source_file_path)

            if not os.path.exists(abs_source_path):
                self._close_hwp()
                return {
                    "success": False,
                    "message": f"원본 파일을 찾을 수 없습니다: {abs_source_path}"
                }

            logger.info(f"Word 파일 열기: {abs_source_path}")

            # Word 파일 열기
            # Open 메서드: (FileName, Format, ReadOnly)
            # Format: "HWP" = HWP 파일로 감지
            # arg3: "" = 보안 옵션
            try:
                # 보안 경고 없이 열기 시도
                result = self.hwp.Open(abs_source_path)
                logger.info(f"Word 파일 열기 결과: {result}")
            except Exception as open_error:
                logger.error(f"파일 열기 실패: {open_error}")
                self._close_hwp()
                return {
                    "success": False,
                    "message": f"파일을 열 수 없습니다: {str(open_error)}"
                }

            # 파일이 완전히 로드될 때까지 대기
            time.sleep(3)

            # 문서 내용 확인
            try:
                page_count = self.hwp.GetPageCount()
                logger.info(f"문서 페이지 수: {page_count}")

                if page_count == 0:
                    logger.warning("문서가 비어있습니다. 파일이 제대로 열리지 않았을 수 있습니다.")
            except Exception as e:
                logger.warning(f"문서 정보 확인 실패: {e}")

            logger.info("Word 파일 열기 완료")

            # HWP 파일로 저장
            output_filename_with_ext = f"{output_filename}.hwp"
            output_path = os.path.join(self.output_dir, output_filename_with_ext)
            absolute_output_path = os.path.abspath(output_path)

            logger.info(f"HWP로 저장 중: {absolute_output_path}")

            # SaveAs 메서드: (FileName, Format)
            # Format: "HWP" = 한글 문서
            # SaveAs는 최대 2-3개의 인자만 받음
            save_result = self.hwp.SaveAs(absolute_output_path, "HWP")

            logger.info(f"HWP 저장 결과: {save_result}")

            # 저장 완료 대기
            time.sleep(1)

            # 한글 종료
            self._close_hwp()

            return {
                "success": True,
                "filename": output_filename_with_ext,
                "file_path": output_path,
                "message": "Word 파일이 성공적으로 HWP로 변환되었습니다."
            }

        except Exception as e:
            logger.error(f"변환 실패: {e}")
            self._close_hwp()
            return {
                "success": False,
                "message": f"변환 실패: {str(e)}"
            }
