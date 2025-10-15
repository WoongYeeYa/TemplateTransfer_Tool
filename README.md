# Template Management System

워드/한글 파일 양식 자동화 시스템

## 주요 기능

### ✅ 구현 완료
- **파일 업로드**: 워드(.docx) 파일 드래그 앤 드롭 업로드
- **자동 분석**: 문서 구조 자동 분석 (문단, 표, 필드 추출)
- **템플릿 관리**: 템플릿 목록 조회, 삭제
- **HWP 생성**: 템플릿 기반 HWP 파일 생성 (기본 구현)
- **다크 테마 UI**: GitHub 스타일의 세련된 다크 테마
- **데이터베이스**: SQLite 기본 지원 (PostgreSQL 전환 가능)

### 🚧 향후 개발 예정
- **HWPX MCP 통합**: 실제 HWP 파일 생성 기능 완성
- **HWP 파일 분석**: hwpx MCP를 사용한 한글 파일 분석
- **AI 필드 인식**: 더 정교한 필드 자동 인식
- **사용자 인증**: 로그인/회원가입 기능

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
│   │   │   ├── document_analyzer.py  # 문서 분석 서비스
│   │   │   └── hwp_generator.py      # HWP 생성 서비스
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
2. Word 파일(.docx)을 드래그 앤 드롭 또는 클릭하여 선택
3. 파일이 자동으로 업로드되고 분석됩니다

### 2. 템플릿 목록 확인
1. "템플릿 목록" 탭 클릭
2. 업로드된 템플릿 카드 형식으로 확인
3. 분석 상태 확인 (uploaded, analyzing, analyzed)

### 3. HWP 파일 생성
1. 템플릿 카드에서 "사용하기" 버튼 클릭
2. 원하는 파일 제목 입력 (선택사항, 기본값: 템플릿 이름)
3. "HWP 파일 생성" 버튼 클릭
4. 파일이 자동으로 다운로드됩니다

## API 엔드포인트

### 템플릿 관리

#### POST /api/templates/upload
템플릿 파일 업로드 및 분석 시작
- **파일 형식**: .docx, .hwp, .doc
- **자동 분석**: 백그라운드에서 문서 분석 수행

#### GET /api/templates/
템플릿 목록 조회

#### GET /api/templates/{template_id}
특정 템플릿 상세 정보 및 분석 결과 조회

#### DELETE /api/templates/{template_id}
템플릿 삭제

### HWP 생성

#### POST /api/hwp/generate
HWP 파일 생성
```json
{
  "template_id": "uuid",
  "filename": "파일명"
}
```

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
- **SQLAlchemy**: ORM (SQLite/PostgreSQL)
- **python-docx**: Word 문서 분석
- **Uvicorn**: ASGI 서버

### 프론트엔드
- **Svelte**: 반응형 UI 프레임워크
- **Vite**: 빌드 도구
- **다크 테마**: GitHub 스타일

## 프로젝트 특징

### 1. 단순하고 직관적인 UI
- 불필요한 입력 필드 제거
- 파일 이름 자동 사용
- 드래그 앤 드롭 지원

### 2. 자동화된 분석
- 파일 업로드 시 자동으로 분석 시작
- 백그라운드 작업으로 사용자 대기 시간 최소화

### 3. 확장 가능한 구조
- MCP 서버 통합 준비
- 데이터베이스 쉽게 전환 가능 (SQLite ↔ PostgreSQL)
- 모듈화된 서비스 구조

## HWPX MCP 통합 (준비 중)

현재 HWP 생성 기능은 기본 구현되어 있으며, HWPX MCP 서버 통합을 통해 실제 HWP 파일 생성이 가능합니다.

### 통합 예정 MCP 도구
- `mcp__hwpx__make_blank`: 빈 HWP 파일 생성
- `mcp__hwpx__add_paragraph`: 문단 추가
- `mcp__hwpx__add_table`: 표 추가
- `mcp__hwpx__save`: 파일 저장
- `mcp__hwpx__read_text`: HWP 파일 읽기

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
- 파일 형식 확인 (.docx, .hwp, .doc만 지원)
- 백엔드 서버 실행 확인
- CORS 설정 확인 (backend/app/main.py)

## 개발 가이드

### 새로운 MCP 도구 추가
1. `backend/app/services/`에 새 서비스 파일 생성
2. MCP 도구 호출 로직 구현
3. API 엔드포인트에서 서비스 호출

### 데이터베이스 모델 수정
1. `backend/app/models/`에서 모델 수정
2. Alembic 마이그레이션 생성
3. 마이그레이션 적용

## 라이선스
MIT

## 지원
문의사항이나 버그 리포트는 GitHub Issues를 통해 제출해주세요.
