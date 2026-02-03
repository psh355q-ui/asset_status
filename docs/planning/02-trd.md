# TRD (기술 요구사항 정의서)

> 개발자/AI 코딩 파트너가 참조하는 기술 문서입니다.
> 기술 표현을 사용하되, "왜 이 선택인지"를 함께 설명합니다.

---

## MVP 캡슐

| # | 항목 | 내용 |
|---|------|------|
| 1 | 목표 | 예금만 하던 투자 초보자가 AI 조언을 받으며 적극적으로 자산을 증식할 수 있도록 지원 |
| 2 | 페르소나 | 30대 후반 직장인, 투자 경험 없음, 가용자산 2억원, 월급 400만원 |
| 3 | 핵심 기능 | FEAT-1: 계좌별 자산현황 조회, FEAT-2: AI 투자조언 (매수/매도 추천) |
| 4 | 성공 지표 (노스스타) | 1년 자산 10% 증가 |
| 5 | 입력 지표 | AI 조언 vs 실제 결과 비교 (백테스팅), 주간 대시보드 확인 3회 이상 |
| 6 | 비기능 요구 | 모바일 반응형 웹, 데이터 영속성 (로컬 PC/NAS), 5초 이내 응답 |
| 7 | Out-of-scope | 증권사 계좌 자동 연동, 자동 매매, 세금 계산, 알림 시스템 |
| 8 | Top 리스크 | AI 조언이 부정확하여 사용자가 손실을 입을 가능성 |
| 9 | 완화/실험 | AI 조언 히스토리 추적, 백테스팅으로 정확도 개선, 면책 고지 |
| 10 | 다음 단계 | API 계약 정의 (Phase 0) 후 TDD 개발 시작 |

---

## 1. 시스템 아키텍처

### 1.1 고수준 아키텍처

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Mobile Web    │────▶│  FastAPI        │────▶│  PostgreSQL     │
│   (React+Vite)  │     │  Backend        │     │  + Docker       │
└─────────────────┘     └─────────────────┘     └─────────────────┘
         │                       │
         │                       ▼
         │              ┌─────────────────┐
         │              │  External APIs  │
         │              │  (yfinance, etc)│
         │              └─────────────────┘
         │
         ▼
  ┌─────────────────┐
  │   AI Service    │
  │  (LLM API)      │
  └─────────────────┘
```

### 1.2 컴포넌트 설명

| 컴포넌트 | 역할 | 왜 이 선택? |
|----------|------|-------------|
| Frontend (React+Vite) | 모바일 반응형 UI, 사용자 상호작용 | 모바일 중심 사용 환경, 빠른 개발, 풍부한 차트 라이브러리 |
| Backend (FastAPI) | API 제공, 비즈니스 로직, AI 조언 생성 | Python 기반 AI 라이브러리 연동 용이, 비동기 처리, 자동 API 문서 |
| Database (PostgreSQL) | 거래 내역, 계좌 정보, AI 조언 히스토리 저장 | 거래 무결성 보장, JSON 컬럼 지원 (AI 분석 결과), 로컬 Docker 실행 |
| External APIs (yfinance) | 주식 현재가, 배당 정보, 뉴스 조회 | 무료, 한국/미국 주식 커버, API 키 불필요 |
| AI Service (LLM) | 투자 조언 생성, 뉴스 분석 | GPT-4 API 또는 로컬 LLM |

---

## 2. 권장 기술 스택

### 2.1 프론트엔드

| 항목 | 선택 | 이유 | 벤더 락인 리스크 |
|------|------|------|--------------------|
| 프레임워크 | React 18+ | 모바일 반응형 웹 최적화, 컴포넌트 재사용성 | 낮음 |
| 빌드 툴 | Vite | 빠른 개발 환경, HMR | 낮음 |
| 언어 | TypeScript 5+ | 타입 안정성, IDE 지원 우수 | - |
| 스타일링 | CSS Modules + Vanilla CSS | 노션 스타일 (담백), 프레임워크 의존성 없음 | 낮음 |
| 상태관리 | Zustand | 경량, 학습 곡선 낮음 | 낮음 |
| HTTP 클라이언트 | Axios | 인터셉터, 에러 처리 용이 | 낮음 |
| 차트 | Recharts | React 친화적, 선언적 API | 낮음 |

### 2.2 백엔드

| 항목 | 선택 | 이유 | 벤더 락인 리스크 |
|------|------|------|--------------------|
| 프레임워크 | FastAPI 0.100+ | Python 기반 AI 라이브러리 연동, 비동기 처리, 자동 API 문서 | 낮음 |
| 언어 | Python 3.11+ | AI/ML 생태계 풍부, yfinance 호환 | - |
| ORM | SQLAlchemy 2.0 | 성숙한 ORM, PostgreSQL 최적화 | 낮음 |
| 검증 | Pydantic v2 | FastAPI 기본 통합, 타입 안정성 | 낮음 |
| AI 라이브러리 | LangChain or OpenAI SDK | LLM 체이닝, 프롬프트 관리 | 중간 (OpenAI API 의존) |
| 주식 데이터 | yfinance | 무료, 한국/미국 주식 커버 | 낮음 (대체 API 존재) |

### 2.3 데이터베이스

| 항목 | 선택 | 이유 |
|------|------|------|
| 메인 DB | PostgreSQL 15+ | 거래 무결성, JSON 컬럼 (AI 분석 결과), Docker 실행 용이 |
| 캐시 | In-memory (Python dict) | MVP는 단일 사용자, Redis 불필요 |

### 2.4 인프라

| 항목 | 선택 | 이유 |
|------|------|------|
| 컨테이너 | Docker + Docker Compose | 로컬 PC/NAS 배포 간편, 환경 일관성 |
| 호스팅 | 로컬 PC/NAS | 개인용, 비용 절감, 데이터 프라이버시 |
| HTTPS | 로컬 인증서 (mkcert) 또는 HTTP | HTTPS는 v2 (외부 접속 시 필요) |

---

## 3. 비기능 요구사항

### 3.1 성능

| 항목 | 요구사항 | 측정 방법 |
|------|----------|----------|
| API 응답 시간 | < 2s (P95) | FastAPI 로깅 |
| 초기 로딩 | < 5s (FCP) | Lighthouse |
| AI 조언 생성 | < 10s | 백엔드 타이머 |

### 3.2 보안

| 항목 | 요구사항 |
|------|----------|
| 인증 | JWT Access Token (개인용이므로 간소화) |
| 비밀번호 | bcrypt 해싱 |
| HTTPS | MVP는 HTTP (로컬 네트워크), v2에서 HTTPS |
| 입력 검증 | Pydantic 서버 측 필수 검증 |
| API 키 보호 | .env 파일 (Git 제외) |

### 3.3 확장성

| 항목 | 현재 | 목표 (v2) |
|------|------|-----------|
| 동시 사용자 | 1명 (개인용) | 가족 3~5명 |
| 데이터 용량 | MVP: 100MB | v2: 1GB |
| 거래 내역 | 1년치 | 10년치 |

---

## 4. 외부 API 연동

### 4.1 주식 데이터

| 서비스 | 용도 | 필수/선택 | 연동 방식 |
|--------|------|----------|----------|
| yfinance | 한국/미국 주식 현재가 조회 | 필수 | Python 라이브러리 |
| yfinance | 배당 정보 조회 | 필수 | Python 라이브러리 |

### 4.2 AI 서비스

| 서비스 | 용도 | 필수/선택 | 비고 |
|--------|------|----------|------|
| OpenAI GPT-4 API | 투자 조언 생성 | 필수 | API 키 필요, 유료 |
| (대안) 로컬 LLM | 투자 조언 생성 | 선택 | Ollama + Llama, 무료 |

### 4.3 뉴스 API

| 서비스 | 용도 | 필수/선택 | 비고 |
|--------|------|----------|------|
| NewsAPI (선택) | 투자 뉴스 수집 | v2 이후 | 무료 플랜 제한적 |

---

## 5. 접근제어·권한 모델

### 5.1 역할 정의

| 역할 | 설명 | 권한 |
|------|------|------|
| Owner | 개인 사용자 (단일 계정) | 전체 CRUD |

(개인용이므로 역할 구분 없음)

### 5.2 권한 매트릭스

| 리소스 | Owner |
|--------|-------|
| 계좌 관리 | O |
| 거래 입력 | O |
| AI 조언 조회 | O |
| 데이터 삭제 | O |

---

## 6. 데이터 생명주기

### 6.1 원칙

- **최소 수집**: 계좌, 거래 내역만 수집
- **명시적 동의**: 개인용이므로 생략
- **보존 기한**: 사용자가 직접 관리

### 6.2 데이터 흐름

```
수집 (거래 입력) → 저장 (PostgreSQL) → 사용 (현황 계산) → 보관 (영구)
```

| 데이터 유형 | 보존 기간 | 삭제/익명화 |
|------------|----------|------------|
| 계좌 정보 | 영구 | 사용자 수동 삭제 |
| 거래 내역 | 영구 | 사용자 수동 삭제 |
| AI 조언 히스토리 | 영구 | 사용자 수동 삭제 |

---

## 7. 테스트 전략 (Contract-First TDD)

### 7.1 개발 방식: Contract-First Development

본 프로젝트는 **계약 우선 개발(Contract-First Development)** 방식을 채택합니다.
BE/FE가 독립적으로 병렬 개발하면서도 통합 시 호환성을 보장합니다.

```
┌─────────────────────────────────────────────────────────────┐
│                    Contract-First 흐름                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. 계약 정의 (Phase 0)                                     │
│     ├─ API 계약: contracts/*.contract.ts                   │
│     ├─ BE 스키마: backend/app/schemas/*.py                 │
│     └─ 타입 동기화: TypeScript ↔ Pydantic                  │
│                                                             │
│  2. 테스트 선행 작성 (🔴 RED)                               │
│     ├─ BE 테스트: tests/api/*.py                           │
│     ├─ FE 테스트: src/__tests__/**/*.test.ts               │
│     └─ 모든 테스트가 실패하는 상태 (정상!)                  │
│                                                             │
│  3. Mock 생성 (FE 독립 개발용)                              │
│     └─ MSW 핸들러: src/mocks/handlers/*.ts                 │
│                                                             │
│  4. 병렬 구현 (🔴→🟢)                                       │
│     ├─ BE: 테스트 통과 목표로 구현                          │
│     └─ FE: Mock API로 개발 → 나중에 실제 API 연결          │
│                                                             │
│  5. 통합 검증                                               │
│     └─ Mock 제거 → E2E 테스트                              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 7.2 테스트 피라미드

| 레벨 | 도구 | 커버리지 목표 | 위치 |
|------|------|-------------|------|
| Unit | pytest / Vitest | ≥ 70% | backend/tests/unit/, frontend/src/__tests__/ |
| Integration | pytest + TestClient | Critical paths | backend/tests/integration/ |
| E2E | Playwright | Key user flows | e2e/ |

### 7.3 테스트 도구

**백엔드:**
| 도구 | 용도 |
|------|------|
| pytest | 테스트 실행 |
| pytest-asyncio | 비동기 테스트 |
| httpx.AsyncClient | FastAPI TestClient |
| pytest-cov | 커버리지 측정 |

**프론트엔드:**
| 도구 | 용도 |
|------|------|
| Vitest | 테스트 실행 |
| React Testing Library | 컴포넌트 테스트 |
| MSW (Mock Service Worker) | API 모킹 |
| Playwright | E2E 테스트 |

### 7.4 계약 파일 구조

```
Asset_Status/
├── contracts/                    # API 계약 (BE/FE 공유)
│   ├── types.ts                 # 공통 타입 정의
│   ├── auth.contract.ts         # 인증 API 계약
│   ├── accounts.contract.ts     # 계좌 API 계약
│   └── transactions.contract.ts # 거래 API 계약
│
├── backend/
│   ├── app/
│   │   ├── schemas/             # Pydantic 스키마 (계약과 동기화)
│   │   │   ├── auth.py
│   │   │   ├── accounts.py
│   │   │   └── transactions.py
│   │   └── routes/              # API 엔드포인트
│   └── tests/
│       ├── unit/                # 단위 테스트
│       └── integration/         # 통합 테스트
│           └── test_api_accounts.py
│
└── frontend/
    ├── src/
    │   ├── mocks/
    │   │   ├── handlers/        # MSW Mock 핸들러
    │   │   │   ├── auth.ts
    │   │   │   └── accounts.ts
    │   │   └── data/            # Mock 데이터
    │   └── __tests__/
    │       └── components/      # 컴포넌트 테스트
    └── e2e/                     # E2E 테스트
        └── dashboard.spec.ts
```

### 7.5 TDD 사이클

모든 기능 개발은 다음 사이클을 따릅니다:

```
🔴 RED    → 실패하는 테스트 먼저 작성 (Phase 0에서 완료)
🟢 GREEN  → 테스트를 통과하는 최소한의 코드 구현
🔵 REFACTOR → 테스트 통과 유지하며 코드 개선
```

### 7.6 품질 게이트

**병합 전 필수 통과:**
- [ ] 모든 단위 테스트 통과
- [ ] 커버리지 ≥ 70%
- [ ] 린트 통과 (ruff / ESLint)
- [ ] 타입 체크 통과 (mypy / tsc)

**검증 명령어:**
```bash
# 백엔드
pytest --cov=app --cov-report=term-missing
ruff check .
mypy app/

# 프론트엔드
npm run test -- --coverage
npm run lint
npm run type-check

# E2E
npx playwright test
```

---

## 8. API 설계 원칙

### 8.1 RESTful 규칙

| 메서드 | 용도 | 예시 |
|--------|------|------|
| GET | 조회 | GET /accounts |
| POST | 생성 | POST /transactions |
| PUT | 전체 수정 | PUT /accounts/{id} |
| PATCH | 부분 수정 | PATCH /accounts/{id} |
| DELETE | 삭제 | DELETE /transactions/{id} |

### 8.2 응답 형식

**성공 응답:**
```json
{
  "data": {
    "accounts": [...]
  },
  "meta": {
    "total": 3
  }
}
```

**에러 응답:**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "거래 수량은 0보다 커야 합니다.",
    "details": [
      { "field": "quantity", "message": "0보다 큰 값을 입력하세요" }
    ]
  }
}
```

### 8.3 API 버저닝

| 방식 | 예시 | 채택 여부 |
|------|------|----------|
| URL 경로 | /api/v1/accounts | 권장 |

---

## 9. 병렬 개발 지원 (Git Worktree)

### 9.1 개요

BE/FE를 완전히 독립된 환경에서 병렬 개발할 때 Git Worktree를 사용합니다.

### 9.2 Worktree 구조

```
~/projects/
├── Asset_Status/              # 메인 (main 브랜치)
├── Asset_Status-accounts-be/  # Worktree: feature/accounts-be
├── Asset_Status-accounts-fe/  # Worktree: feature/accounts-fe
├── Asset_Status-ai-be/        # Worktree: feature/ai-be
└── Asset_Status-ai-fe/        # Worktree: feature/ai-fe
```

### 9.3 명령어

```bash
# Worktree 생성
git worktree add ../Asset_Status-accounts-be -b feature/accounts-be
git worktree add ../Asset_Status-accounts-fe -b feature/accounts-fe

# 각 Worktree에서 독립 작업
cd ../Asset_Status-accounts-be && pytest tests/
cd ../Asset_Status-accounts-fe && npm run test

# 테스트 통과 후 병합
git checkout main
git merge --no-ff feature/accounts-be
git merge --no-ff feature/accounts-fe

# Worktree 정리
git worktree remove ../Asset_Status-accounts-be
git worktree remove ../Asset_Status-accounts-fe
```

### 9.4 병합 규칙

| 조건 | 병합 가능 |
|------|----------|
| 단위 테스트 통과 (🟢) | 필수 |
| 커버리지 ≥ 70% | 필수 |
| 린트/타입 체크 통과 | 필수 |

---

## Decision Log 참조

| ID | 항목 | 선택 | 이유 |
|----|------|------|------|
| T-01 | 백엔드 프레임워크 | FastAPI | Python AI 생태계, 비동기, 자동 API 문서 |
| T-02 | 프론트엔드 | React + Vite | 모바일 반응형, 빠른 개발, 차트 라이브러리 풍부 |
| T-03 | 데이터베이스 | PostgreSQL | 거래 무결성, JSON 컬럼, Docker 실행 용이 |
| T-04 | 주식 데이터 API | yfinance | 무료, 한국/미국 주식 커버, API 키 불필요 |
| T-05 | AI 서비스 | OpenAI GPT-4 API | 높은 정확도, LangChain 호환 |
| T-06 | 배포 환경 | Docker Compose | 로컬 PC/NAS 간편 배포 |
| T-07 | 개발 방식 | Contract-First TDD | BE/FE 병렬 개발, 통합 리스크 최소화 |
