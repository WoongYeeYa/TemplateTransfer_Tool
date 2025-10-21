# DOCX to HWP 변환기 - Python 레거시 버전

이 폴더는 Python + COM API 기반 DOCX to HWP 변환기의 레거시 버전입니다.

**⚠️ 주의: 이 버전은 더 이상 권장되지 않습니다.**

새로운 Java 버전을 사용하세요: `../backend-java/`

---

## ❌ 왜 레거시인가?

### Python COM API 방식의 한계

1. **Windows 전용**
   - Hancom Office 설치 필수
   - Windows에서만 동작

2. **불안정한 기능**
   - ❌ 셀 병합 실패 (`HTableCellBlock` 오류)
   - ❌ 셀 배경색 실패 (서버 예외 오류)
   - ❌ 복잡한 표 변환 실패

3. **느린 속도**
   - COM API 백그라운드 프로세스
   - HWP 프로그램 자동화 방식

4. **유지보수 어려움**
   - Windows API 의존성
   - Hancom Office 버전 호환성 문제

---

## ✅ 새 버전 사용 권장

### Java + hwplib 방식

```bash
# 프로젝트 루트로 이동
cd ..

# 자동 설치 및 실행
빠른_시작.bat
```

**장점:**
- ✅ Hancom Office 불필요
- ✅ 크로스 플랫폼 (Windows, Linux, macOS)
- ✅ 안정적인 셀 병합
- ✅ 빠른 변환 속도

자세한 내용: `../설치_가이드.md` 참고

---

## 📂 폴더 구조

```
legacy-python/
├── backend/              # Python FastAPI 백엔드
│   ├── main.py          # FastAPI 서버
│   ├── hwp_converter.py # COM API 변환 로직
│   └── requirements.txt # Python 의존성
│
├── frontend/            # 프론트엔드 (HTML/CSS/JS)
│   ├── index.html
│   ├── style.css
│   └── app.js
│
├── start.bat            # 통합 메뉴
├── start_server.bat     # 서버 시작
├── stop_server.bat      # 서버 종료
├── install.bat          # 의존성 설치
├── open_browser.bat     # 브라우저 열기
│
├── test_*.py            # 테스트 스크립트들
├── test_*.docx          # 테스트 파일들
├── test_*.hwp           # 테스트 결과들
│
├── USAGE.md             # 사용법
├── 시작하기.txt          # 빠른 시작 가이드
└── README.md            # 이 파일
```

---

## 🔧 시스템 요구사항 (레거시)

- Windows OS
- **Hancom Office 한글 2014 이상 설치 필수**
- Python 3.8 이상

---

## 🚀 사용 방법 (레거시)

### 1. Python 의존성 설치

```bash
install.bat
```

또는

```bash
cd backend
pip install -r requirements.txt
```

### 2. 서버 실행

```bash
start_server.bat
```

또는

```bash
cd backend
python main.py
```

### 3. 브라우저 접속

```
http://localhost:8000
```

---

## 🐛 알려진 문제

### 셀 병합 실패
```
ERROR - 셀 병합 실패: <unknown>.HTableCellBlock
```

**원인**: COM API의 HTableCellBlock 파라미터 미지원

**해결**: Java 버전 사용 권장

---

### 셀 배경색 실패
```
WARNING - 셀 배경색 설정 실패: (-2147417851, '서버에서 예외 오류가 발생했습니다.', None, None)
```

**원인**: COM API의 CellBorderFill 동작 불안정

**해결**: Java 버전에서 추후 지원 예정

---

### 복잡한 표 변환 실패

**증상**:
- 간단한 표는 정상 변환
- 셀 병합이 있는 표는 완전히 깨짐

**원인**: COM API 한계

**해결**: Java 버전 사용 (TableCellMerger로 완벽 지원)

---

## 📊 기능 비교

| 기능 | Python (이 폴더) | Java (권장) |
|------|----------------|-------------|
| 텍스트 변환 | ✅ | ✅ |
| 간단한 표 | ✅ | ✅ |
| **셀 병합** | ❌ | ✅ |
| **셀 배경색** | ❌ | 🚧 |
| 텍스트 색상 | ✅ | 🚧 |
| 문단 정렬 | ✅ | 🚧 |
| 들여쓰기 | ✅ | 🚧 |
| Hancom Office 필요 | ✅ 필요 | ❌ 불필요 |
| 크로스 플랫폼 | ❌ | ✅ |
| 속도 | 느림 | 빠름 |

---

## 🔄 마이그레이션

### Python → Java 전환

1. 프로젝트 루트로 이동
   ```bash
   cd ..
   ```

2. Java 버전 실행
   ```bash
   빠른_시작.bat
   ```

3. 기존 Python 서버 종료
   ```bash
   cd legacy-python
   stop_server.bat
   ```

자세한 내용: `../JAVA_MIGRATION_GUIDE.md`

---

## 📝 테스트 파일

### 성공한 테스트
- `test_formatting.docx` → `test_formatting.hwp` ✅
  - 텍스트 색상
  - 문단 정렬
  - 들여쓰기/내어쓰기

- `test_simple_table.docx` → `test_simple_table.hwp` ✅
  - 간단한 표 (셀 병합 없음)

### 실패한 테스트
- `test_complex_table.docx` ❌
  - 셀 병합 (5칸 가로, 2칸 세로, 2x2 블록)
  - 셀 배경색
  - **Java 버전에서는 성공!**

---

## 📞 문의

이 레거시 버전 대신 새 Java 버전을 사용하세요:

```bash
cd ..
빠른_시작.bat
```

---

## 📄 라이선스

- Python-docx: MIT
- FastAPI: MIT
- Hancom Office COM API: Hancom Inc.

---

## 🗓️ 버전 히스토리

### v1.1.0 (레거시 - 2025-10-21)
- 텍스트 색상, 정렬, 들여쓰기 지원
- 간단한 표 변환 지원
- ❌ 셀 병합, 배경색 미지원

### v1.0.0 (초기 버전)
- 기본 DOCX to HWP 변환
- 템플릿 관리

---

**⚠️ 다시 한 번: 새로운 Java 버전(`../backend-java/`)을 사용하세요!**
