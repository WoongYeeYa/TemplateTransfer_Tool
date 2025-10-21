"""
복잡한 표 변환 테스트
"""
import sys
import os

# 백엔드 모듈 경로 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from hwp_converter import HWPConverter

def test_table_conversion():
    """복잡한 표를 HWP로 변환"""
    docx_path = "test_complex_table.docx"
    hwp_path = "test_complex_table.hwp"

    if not os.path.exists(docx_path):
        print(f"[ERROR] 테스트 파일을 찾을 수 없습니다: {docx_path}")
        return False

    print("=" * 60)
    print("복잡한 표 DOCX to HWP 변환 테스트")
    print("=" * 60)
    print(f"입력 파일: {docx_path}")
    print(f"출력 파일: {hwp_path}")
    print()

    converter = HWPConverter()

    # 한컴오피스 설치 확인
    is_installed, version = converter.check_hwp_installed()
    if not is_installed:
        print("[ERROR] 한컴오피스가 설치되지 않았거나 연동할 수 없습니다.")
        return False

    print(f"[OK] 한컴오피스 버전: {version}")
    print()

    # 변환 실행
    print("변환 중...")
    print()
    success = converter.convert_docx_to_hwp(docx_path, hwp_path)

    if success:
        if os.path.exists(hwp_path):
            file_size = os.path.getsize(hwp_path)
            print()
            print("=" * 60)
            print("[OK] 변환 성공!")
            print("=" * 60)
            print(f"생성된 파일: {hwp_path}")
            print(f"파일 크기: {file_size:,} bytes")
            print()
            print("테스트 확인 항목:")
            print("  1. 셀 병합 (가로, 세로, 2x2 블록)")
            print("  2. 셀 배경색")
            print("  3. 표 안의 정렬")
            print("  4. 폰트 색깔")
            print("  5. 폰트 크기")
            print()
            print("생성된 HWP 파일을 열어서 표가 제대로 변환되었는지 확인하세요.")
            return True
        else:
            print("[ERROR] 변환은 성공했지만 파일이 생성되지 않았습니다.")
            return False
    else:
        print("[ERROR] 변환 실패")
        return False

if __name__ == "__main__":
    test_table_conversion()
