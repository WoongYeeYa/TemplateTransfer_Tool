"""
한글 COM API를 사용한 HWP 파일 생성
한글 2018에서 열 수 있는 HWP 5.0 형식으로 생성
"""
import os
import logging
from typing import Dict, Any
import win32com.client
import pythoncom

logger = logging.getLogger(__name__)


class HwpComGenerator:
    """한글 COM API를 사용한 HWP 생성기"""

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

            # 보안 경고 자동 허용 설정
            self.hwp.SetMessageBoxMode(0x00010000)  # 모든 메시지 박스 자동 허용

            # 한글 창 숨기기 (비가시 모드)
            self.hwp.XHwpWindows.Item(0).Visible = False

            logger.info("한글 COM 초기화 완료 (비가시 모드)")
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

    async def generate_hwp(
        self,
        template: Dict[str, Any],
        filename: str
    ) -> Dict[str, Any]:
        """
        HWP 파일 생성

        Args:
            template: 템플릿 정보
            filename: 생성할 파일 이름

        Returns:
            생성 결과 딕셔너리
        """
        try:
            # 분석 결과 가져오기
            analysis_result = template.get("analysis_result")

            if not analysis_result:
                return {
                    "success": False,
                    "message": "템플릿 분석이 완료되지 않았습니다."
                }

            # 한글 초기화
            if not self._initialize_hwp():
                return {
                    "success": False,
                    "message": "한글 프로그램을 시작할 수 없습니다. 한글이 설치되어 있는지 확인하세요."
                }

            # 새 문서 생성
            self.hwp.Open("", "")
            logger.info("새 문서 생성")

            # 문서 제목 추가 (템플릿 이름)
            doc_title = template.get("name", "제목 없음")
            self._add_text(doc_title, bold=True, font_size=14)
            self._add_paragraph()
            self._add_paragraph()

            # 문단 추가
            paragraphs = analysis_result.get("paragraphs", [])
            logger.info(f"{len(paragraphs)}개 문단 추가 중...")

            for para in paragraphs:
                text = para.get("text", "")
                style = para.get("style", "Normal")

                # 스타일에 따라 볼드 처리
                is_bold = "Heading" in style or "Title" in style
                self._add_text(text, bold=is_bold)
                self._add_paragraph()

            # 표 추가
            tables = analysis_result.get("tables", [])
            if tables:
                logger.info(f"{len(tables)}개 표 추가 중...")

                for table_idx, table in enumerate(tables):
                    rows = table.get("rows", 0)
                    cols = table.get("cols", 0)
                    cells = table.get("cells", [])

                    if rows > 0 and cols > 0:
                        # 표 삽입
                        self._add_table(rows, cols)

                        # 표 내용 채우기
                        self._fill_table_content(cells)

                        # 표 다음 빈 줄
                        self._add_paragraph()

            # 파일 저장
            output_filename = f"{filename}.hwp"
            output_path = os.path.join(self.output_dir, output_filename)
            absolute_path = os.path.abspath(output_path)

            # HWP 5.0 형식으로 저장
            self.hwp.SaveAs(absolute_path, "HWP")
            logger.info(f"HWP 파일 저장: {absolute_path}")

            # 한글 종료
            self._close_hwp()

            return {
                "success": True,
                "filename": output_filename,
                "file_path": output_path,
                "message": "HWP 파일이 성공적으로 생성되었습니다."
            }

        except Exception as e:
            logger.error(f"HWP 생성 실패: {e}")
            self._close_hwp()
            return {
                "success": False,
                "message": f"HWP 생성 실패: {str(e)}"
            }

    def _add_text(self, text: str, bold: bool = False, font_size: int = 10):
        """텍스트 추가"""
        try:
            # 간단한 방법: InsertText 사용
            act = self.hwp.CreateAction("InsertText")
            pset = act.CreateSet()
            act.GetDefault(pset)
            pset.SetItem("Text", text)
            act.Execute(pset)

        except Exception as e:
            logger.error(f"텍스트 추가 실패: {e}")

    def _add_paragraph(self):
        """문단 나누기 (Enter)"""
        try:
            self.hwp.HAction.Run("BreakPara")
        except Exception as e:
            logger.error(f"문단 나누기 실패: {e}")

    def _add_table(self, rows: int, cols: int):
        """표 삽입"""
        try:
            # 간단한 방법: Insert 키 조합 사용
            act = self.hwp.CreateAction("TableCreate")
            pset = act.CreateSet()
            act.GetDefault(pset)
            pset.SetItem("Rows", rows)
            pset.SetItem("Cols", cols)
            pset.SetItem("WidthType", 2)  # 0: 임의, 1: 좁게, 2: 넓게
            pset.SetItem("HeightType", 0)  # 0: 자동
            act.Execute(pset)
            logger.info(f"표 삽입 완료: {rows}행 x {cols}열")
        except Exception as e:
            logger.error(f"표 삽입 실패: {e}")

    def _fill_table_content(self, cells: list):
        """표 내용 채우기"""
        try:
            if not cells:
                return

            # 표의 첫 셀로 이동
            self.hwp.Run("TableLeftTop")

            for row_idx, row in enumerate(cells):
                for col_idx, cell_text in enumerate(row):
                    # 현재 셀에 텍스트 입력
                    if cell_text:
                        act = self.hwp.CreateAction("InsertText")
                        pset = act.CreateSet()
                        act.GetDefault(pset)
                        pset.SetItem("Text", cell_text)
                        act.Execute(pset)

                    # 다음 셀로 이동 (마지막 셀이 아닌 경우)
                    if col_idx < len(row) - 1:
                        self.hwp.Run("TableRightCell")
                    elif row_idx < len(cells) - 1:
                        # 다음 행의 첫 셀로 이동
                        self.hwp.Run("TableDownCell")

            # 표 밖으로 이동
            self.hwp.Run("TableOutRight")
            logger.info("표 내용 채우기 완료")

        except Exception as e:
            logger.error(f"표 내용 채우기 실패: {e}")
