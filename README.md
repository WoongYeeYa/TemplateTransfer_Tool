# Template Management System

워드 파일을 HWP 파일로 변환하는 시스템

## 주요 기능

### ✅ 구현 완료
- **파일 업로드**: 워드(.doc, .docx) 파일 드래그 앤 드롭 업로드
- **직접 변환**: 문서 분석 없이 원본 포맷을 그대로 HWP로 변환
- **템플릿 관리**: 템플릿 목록 조회, 삭제
- **HWP 파일 생성**: 한글 COM API를 사용한 실제 HWP 5.0 파일 생성
- **한글 2018 호환**: 한글 2018에서 완벽하게 열리는 HWP 파일 생성
- **포맷 유지**: 표, 서식, 레이아웃 등 모든 문서 요소 완벽 보존
- **다크 테마 UI**: GitHub 스타일의 세련된 다크 테마
- **간편한 사용**: 업로드 → 변환 → 다운로드 3단계로 완료

### 🚧 향후 개발 예정
- **사용자 인증**: 로그인/회원가입 기능
- **변환 이력**: 변환 기록 관리
- **배치 변환**: 여러 파일 동시 변환

## 시스템 구조

```
template_management/
├── backend/                    # FastAPI 백엔드
│   ├── app/
│   │   ├── main.py            # API 메인 엔트리
│   │   ├── api/               # API 엔드포인트
│   │   │   ├── templates.py   # 템플릿 관리 API
│   │   │   └── hwp.py         # HWP 생성/다운로드 API
│   │   ├── services/          # 비즈니스 로직
│   │   │   └── doc_to_hwp_converter.py  # DOC → HWP 직접 변환 서비스
│   │   ├── models/            # 데이터베이스 모델
│   │   │   └── template.py    # Template 모델
│   │   └── core/              # 핵심 설정
│   │       └── database.py    # 데이터베이스 설정
│   └── requirements.txt
├── frontend/                   # Svelte 프론트엔드
│   ├── src/
│   │   ├── App.svelte         # 메인 앱
│   │   └── lib/               # 컴포넌트
│   │       ├── TemplateUpload.svelte    # 업로드 UI
│   │       ├── TemplateList.svelte      # 목록 UI
│   │       └── HwpGenerator.svelte      # HWP 생성 UI
│   └── package.json
├── uploads/                   # 업로드된 파일
├── outputs/                   # 생성된 HWP 파일
├── start-all.bat             # 전체 서버 실행 스크립트
├── start-backend.bat         # 백엔드 실행 스크립트
└── start-frontend.bat        # 프론트엔드 실행 스크립트
```

## 빠른 시작

### 사전 요구사항
- Python 3.8 이상
- Node.js 16 이상

### 1. 의존성 설치

**백엔드:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**프론트엔드:**
```bash
cd frontend
npm install
```

### 2. 서버 실행

#### 방법 1: 한 번에 실행 (추천)
```bash
start-all.bat
```

#### 방법 2: 개별 실행
```bash
# 백엔드
start-backend.bat

# 프론트엔드 (새 터미널)
start-frontend.bat
```

#### 방법 3: 수동 실행
```bash
# 백엔드
cd backend
venv\Scripts\activate
python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload

# 프론트엔드 (새 터미널)
cd frontend
npm run dev
```

### 3. 접속
- **프론트엔드 UI**: http://localhost:5174
- **백엔드 API**: http://localhost:8001
- **API 문서**: http://localhost:8001/docs

## 사용 방법

### 1. 템플릿 업로드
1. "템플릿 업로드" 탭 클릭
2. Word 파일(.doc 또는 .docx)을 드래그 앤 드롭 또는 클릭하여 선택
3. 파일이 자동으로 업로드됩니다

### 2. 템플릿 목록 확인
1. "템플릿 목록" 탭 클릭
2. 업로드된 템플릿 카드 형식으로 확인
3. 상태 확인: "변환 가능" 표시

### 3. HWP 파일 변환 및 다운로드
1. 템플릿 카드에서 "사용하기" 버튼 클릭
2. 원하는 파일 이름 입력 (선택사항, 기본값: 템플릿 이름)
3. "HWP 파일 생성" 버튼 클릭
4. 변환된 HWP 파일이 자동으로 다운로드됩니다

**중요**: 변환된 HWP 파일은 원본 문서의 모든 내용, 표, 서식, 레이아웃을 그대로 유지합니다.

## API 엔드포인트

### 템플릿 관리

#### POST /api/templates/upload
템플릿 파일 업로드
- **파일 형식**: .doc, .docx
- **처리**: 파일 저장 후 즉시 변환 가능

#### GET /api/templates/
템플릿 목록 조회

#### GET /api/templates/{template_id}
특정 템플릿 상세 정보 조회

#### DELETE /api/templates/{template_id}
템플릿 삭제

### HWP 생성

#### POST /api/hwp/generate
DOC/DOCX 파일을 HWP로 직접 변환
```json
{
  "template_id": "uuid",
  "filename": "파일명"
}
```
- 원본 파일의 모든 내용을 HWP로 변환
- 표, 서식, 레이아웃 완벽 보존

#### GET /api/hwp/download/{filename}
생성된 HWP 파일 다운로드

## 데이터베이스 설정

### SQLite (기본)
별도 설치 없이 즉시 사용 가능합니다. 데이터는 `template_management.db` 파일에 저장됩니다.

### PostgreSQL (선택사항)
PostgreSQL을 사용하려면:

1. PostgreSQL 설치 및 데이터베이스 생성
```sql
CREATE DATABASE template_management;
```

2. 환경 변수 설정 또는 `backend/app/core/database.py` 수정
```python
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/template_management"
```

3. 의존성 재설치
```bash
cd backend
venv\Scripts\activate
pip install -r requirements.txt
```

## 기술 스택

### 백엔드
- **FastAPI**: Python 웹 프레임워크
- **pywin32**: Windows COM API (한글 제어)
- **한글 COM API**: DOC/DOCX → HWP 변환
- **Uvicorn**: ASGI 서버

### 프론트엔드
- **Svelte**: 반응형 UI 프레임워크
- **Vite**: 빌드 도구
- **다크 테마**: GitHub 스타일

## 프로젝트 특징

### 1. 단순하고 빠른 변환
- 문서 분석 없이 직접 변환
- 원본 포맷 100% 보존
- 빠른 변환 속도

### 2. 직관적인 UI
- 업로드 → 변환 → 다운로드 3단계
- 파일 이름 자동 사용
- 드래그 앤 드롭 지원

### 3. 안정적인 기술 스택
- 한글 COM API로 완벽한 호환성
- HWP 5.0 형식 (한글 2018 지원)
- 모듈화된 서비스 구조

## 기술 상세

### DOC/DOCX → HWP 변환 원리
1. **한글 COM API 활용**: Windows COM을 통해 한글 프로그램을 프로그래밍 방식으로 제어
2. **직접 변환**: 한글 프로그램이 Word 파일을 직접 열고 HWP로 저장
3. **포맷 보존**: 한글 프로그램의 내장 변환 기능 사용으로 완벽한 호환성 보장
4. **HWP 5.0 형식**: 한글 2018과 호환되는 형식으로 저장

### 핵심 코드 (backend/app/services/doc_to_hwp_converter.py)
```python
# 한글 COM API 초기화
self.hwp = win32com.client.gencache.EnsureDispatch("HWPFrame.HwpObject")

# Word 파일 열기
self.hwp.Open(abs_source_path, "")

# HWP 형식으로 저장
self.hwp.SaveAs(absolute_output_path, "HWP")
```

## 문제 해결

### 포트 충돌
백엔드 기본 포트는 8001입니다. 포트가 사용 중이면:
```bash
cd backend
python -m uvicorn app.main:app --port 8002
```

### 데이터베이스 초기화
SQLite 파일을 삭제하고 재시작:
```bash
del template_management.db
start-backend.bat
```

### 파일 업로드 오류
- 파일 형식 확인 (.doc, .docx만 지원)
- 백엔드 서버 실행 확인
- CORS 설정 확인 (backend/app/main.py)

### 변환 오류
- 한글 프로그램이 설치되어 있는지 확인
- 한글 프로그램이 다른 곳에서 실행 중이 아닌지 확인
- 원본 Word 파일이 손상되지 않았는지 확인

## 시스템 요구사항

- **운영체제**: Windows (한글 COM API 필요)
- **한글 프로그램**: 한글 2018 이상 설치 필수
- **Python**: 3.8 이상
- **Node.js**: 16 이상

## 개발 가이드

### 변환 로직 수정
변환 로직은 `backend/app/services/doc_to_hwp_converter.py`에 구현되어 있습니다.
한글 COM API의 다양한 메서드를 활용하여 변환 옵션을 추가할 수 있습니다.

## 라이선스
MIT

## 지원
문의사항이나 버그 리포트는 GitHub Issues를 통해 제출해주세요.
