"""
간단한 표 변환 테스트
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from hwp_converter import HWPConverter

def test_simple_table():
    """간단한 표를 HWP로 변환"""
    docx_path = "test_simple_table.docx"
    hwp_path = "test_simple_table.hwp"

    if not os.path.exists(docx_path):
        print(f"[ERROR] 파일을 찾을 수 없습니다: {docx_path}")
        return False

    print("=" * 60)
    print("간단한 표 DOCX to HWP 변환 테스트")
    print("=" * 60)
    print(f"입력: {docx_path}")
    print(f"출력: {hwp_path}")
    print()

    converter = HWPConverter()

    # 한컴오피스 확인
    is_installed, version = converter.check_hwp_installed()
    if not is_installed:
        print("[ERROR] 한컴오피스가 설치되지 않았습니다.")
        return False

    print(f"[OK] 한컴오피스: {version}")
    print()

    # 변환
    print("변환 중...")
    success = converter.convert_docx_to_hwp(docx_path, hwp_path)

    if success and os.path.exists(hwp_path):
        file_size = os.path.getsize(hwp_path)
        print()
        print("=" * 60)
        print("[OK] 변환 성공!")
        print("=" * 60)
        print(f"파일: {hwp_path} ({file_size:,} bytes)")
        print()
        print("HWP 파일을 열어서 표가 제대로 나오는지 확인하세요.")
        return True
    else:
        print("[ERROR] 변환 실패")
        return False

if __name__ == "__main__":
    test_simple_table()
