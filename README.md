# 자산관리현황 (Asset Status)

개인 투자 자산을 통합 관리하고 AI 기반 투자 조언을 제공하는 웹 애플리케이션입니다.

## 🎯 프로젝트 목표

- 모든 투자 계좌를 한눈에 조회
- AI 기반 투자 조언 (매수/매도 추천)
- 거래 내역 기록 및 수익률 추적
- 모바일 최적화 UI (노션 스타일)

## 🛠 기술 스택

### Backend
- **FastAPI** - Python 3.11+ 비동기 웹 프레임워크
- **SQLAlchemy 2.0** - ORM (async)
- **PostgreSQL 15+** - 데이터베이스
- **PGVector** - AI/벡터 검색
- **Redis** - 캐싱
- **Alembic** - 마이그레이션

### Frontend
- **React 18+** - UI 라이브러리
- **Vite** - 빌드 툴
- **TypeScript 5+** - 타입 안전성
- **Zustand** - 상태 관리
- **Recharts** - 차트
- **Lucide-react** - 아이콘

### External APIs
- **yfinance** - 주식 시세 조회
- **OpenAI GPT-4** - AI 투자 조언

## 📁 프로젝트 구조

```
Asset_Status/
├── backend/                 # FastAPI 백엔드
│   ├── app/
│   │   ├── models/          # SQLAlchemy 모델
│   │   ├── routes/          # API 엔드포인트
│   │   ├── schemas/         # Pydantic 스키마
│   │   └── services/        # 비즈니스 로직
│   ├── tests/               # Pytest 테스트
│   └── alembic/             # DB 마이그레이션
├── frontend/                # React 프론트엔드
│   ├── src/
│   │   ├── components/      # 재사용 컴포넌트
│   │   ├── pages/           # 페이지
│   │   ├── services/        # API 호출
│   │   └── stores/          # Zustand 스토어
│   └── e2e/                 # Playwright E2E 테스트
├── docs/planning/           # 기획 문서
│   ├── 01-prd.md            # 제품 요구사항
│   ├── 02-trd.md            # 기술 요구사항
│   ├── 04-database-design.md # DB 설계
│   └── 06-tasks.md          # 개발 태스크
├── .claude/                 # AI 에이전트 팀
│   ├── agents/              # 전문가 에이전트
│   └── commands/            # 오케스트레이터
└── docker-compose.yml       # Docker 환경
```

## 🚀 시작하기

### 1. 환경 변수 설정

```bash
cp .env.example .env
# .env 파일을 열어 필수 값 입력 (OPENAI_API_KEY 등)
```

### 2. Docker 실행

```bash
docker compose up -d
```

### 3. 백엔드 실행

```bash
cd backend
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

→ API: http://localhost:8000
→ Swagger Docs: http://localhost:8000/docs

### 4. 프론트엔드 실행

```bash
cd frontend
npm install
npm run dev
```

→ UI: http://localhost:5173

## 📋 개발 워크플로우

이 프로젝트는 **Contract-First TDD** 방식으로 개발합니다.

### Phase 0: 프로젝트 셋업 (현재)
- Docker Compose 환경 구성 ✅
- 기획 문서 작성 ✅
- 에이전트 팀 구성 ✅

### Phase 1: FEAT-0 온보딩/로그인
- 사용자 인증 (JWT)
- 로그인/회원가입 UI

### Phase 2: FEAT-1 계좌 관리
- 계좌 CRUD API
- 거래 입력 UI

### Phase 3: FEAT-1 자산 현황
- 보유 수량 계산
- 실시간 시세 조회
- 대시보드 UI

### Phase 4: FEAT-2 AI 투자 조언
- OpenAI 연동
- 조언 히스토리
- AI 조언 UI

### Phase 5: 통합 & 배포
- E2E 테스트
- Docker 통합 테스트

## 👥 AI 에이전트 팀

이 프로젝트는 여러 AI 전문가 에이전트가 협업합니다:

- **Orchestrator** - 작업 분석 및 에이전트들 조율
- **Backend Specialist** - FastAPI, DB 로직
- **Frontend Specialist** - React UI, 상태 관리
- **Database Specialist** - PostgreSQL, 마이그레이션
- **Test Specialist** - Pytest, Vitest, E2E 테스트

### 오케스트레이터 사용법

```
/orchestrate T1.1 구현해줘
```

## 📖 주요 문서

- [PRD](docs/planning/01-prd.md) - 제품 요구사항 정의서
- [TRD](docs/planning/02-trd.md) - 기술 요구사항 정의서
- [User Flow](docs/planning/03-user-flow.md) - 사용자 흐름도
- [Database Design](docs/planning/04-database-design.md) - 데이터베이스 설계
- [Design System](docs/planning/05-design-system.md) - 디자인 시스템
- [TASKS](docs/planning/06-tasks.md) - 개발 태스크 목록
- [Coding Convention](docs/planning/07-coding-convention.md) - 코딩 규칙

## 🧪 테스트

### 백엔드 테스트

```bash
cd backend
pytest tests/ -v --cov=app
```

### 프론트엔드 테스트

```bash
cd frontend
npm run test
```

### E2E 테스트

```bash
cd frontend
npx playwright test
```

## ⚠️ 면책 고지

본 애플리케이션의 AI 투자 조언은 **참고용**이며, 실제 투자 결정은 사용자 본인의 책임입니다.
AI 조언의 정확도는 보장되지 않으며, 투자 손실에 대한 책임은 사용자에게 있습니다.

## 📝 라이선스

Personal Use Only - 개인용 프로젝트
