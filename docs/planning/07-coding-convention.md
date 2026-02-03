# Coding Convention & AI Collaboration Guide

> 고품질/유지보수/보안을 위한 인간-AI 협업 운영 지침서입니다.

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

## 1. 핵심 원칙

### 1.1 신뢰하되, 검증하라 (Trust, but Verify)

AI가 생성한 코드는 반드시 검증해야 합니다:

- [x] 코드 리뷰: 생성된 코드 직접 확인
- [x] 테스트 실행: 자동화 테스트 통과 확인
- [x] 보안 검토: 민감 정보 노출 여부 확인
- [x] 동작 확인: 실제로 실행하여 기대 동작 확인

### 1.2 최종 책임은 인간에게

- AI는 도구이고, 최종 결정과 책임은 개발자에게 있습니다
- 이해하지 못하는 코드는 사용하지 않습니다
- 의심스러운 부분은 반드시 질문합니다

---

## 2. 프로젝트 구조

### 2.1 디렉토리 구조

```
Asset_Status/
├── frontend/
│   ├── src/
│   │   ├── components/     # 재사용 컴포넌트
│   │   ├── pages/          # 페이지 컴포넌트
│   │   ├── hooks/          # 커스텀 훅
│   │   ├── utils/          # 유틸리티 함수
│   │   ├── services/       # API 호출
│   │   ├── stores/         # Zustand 스토어
│   │   ├── types/          # TypeScript 타입
│   │   └── mocks/          # MSW Mock 핸들러
│   ├── tests/
│   └── e2e/
├── backend/
│   ├── app/
│   │   ├── models/         # SQLAlchemy 모델
│   │   ├── routes/         # FastAPI 라우트
│   │   ├── schemas/        # Pydantic 스키마
│   │   ├── services/       # 비즈니스 로직
│   │   └── utils/          # 유틸리티
│   └── tests/
│       ├── unit/
│       └── integration/
├── contracts/              # API 계약 (BE/FE 공유)
├── docs/
│   └── planning/           # 기획 문서 (Socrates 산출물)
├── docker-compose.yml
└── .env.example
```

### 2.2 네이밍 규칙

| 대상 | 규칙 | 예시 |
|------|------|------|
| 파일 (컴포넌트) | PascalCase | `Dashboard.tsx`, `AccountCard.tsx` |
| 파일 (유틸) | camelCase | `formatCurrency.ts`, `calculateReturn.ts` |
| 파일 (Python) | snake_case | `account_service.py`, `ai_advisor.py` |
| 컴포넌트 | PascalCase | `Dashboard`, `AccountCard` |
| 함수/변수 (JS/TS) | camelCase | `getAccounts`, `totalAssets` |
| 함수 (Python) | snake_case | `get_accounts`, `calculate_holding` |
| 상수 | UPPER_SNAKE | `MAX_ACCOUNTS`, `API_TIMEOUT` |
| CSS 클래스 | kebab-case | `account-card`, `btn-primary` |

---

## 3. 아키텍처 원칙

### 3.1 뼈대 먼저 (Skeleton First)

1. 전체 구조를 먼저 잡고
2. 빈 함수/컴포넌트로 스켈레톤 생성
3. 하나씩 구현 채워나가기

### 3.2 작은 모듈로 분해

- 한 파일에 200줄 이하 권장
- 한 함수에 50줄 이하 권장
- 한 컴포넌트에 100줄 이하 권장

### 3.3 관심사 분리

| 레이어 | 역할 | 예시 |
|--------|------|------|
| UI | 화면 표시 | React 컴포넌트 |
| 상태 | 데이터 관리 | Zustand 스토어 |
| 서비스 | API 통신 | Axios API 클라이언트 |
| 유틸 | 순수 함수 | 날짜 포맷, 금액 계산 |

---

## 4. AI 소통 원칙

### 4.1 하나의 채팅 = 하나의 작업

- 한 번에 하나의 명확한 작업만 요청
- 작업 완료 후 다음 작업 진행
- 컨텍스트가 길어지면 새 대화 시작

### 4.2 컨텍스트 명시

**좋은 예:**
> "TASKS.md의 T1.1을 구현해주세요.
> Database Design의 ACCOUNT 엔티티를 참조하고,
> TRD의 FastAPI + PostgreSQL 스택을 따라주세요."

**나쁜 예:**
> "계좌 기능 만들어줘"

### 4.3 기존 코드 재사용

- 새로 만들기 전에 기존 코드 확인 요청
- 중복 코드 방지
- 일관성 유지

### 4.4 프롬프트 템플릿

```
## 작업
{{무엇을 해야 하는지}}

## 참조 문서
- {{문서명}} 섹션 {{번호}}

## 제약 조건
- {{지켜야 할 것}}

## 예상 결과
- {{생성될 파일}}
- {{기대 동작}}
```

---

## 5. 보안 체크리스트

### 5.1 절대 금지

- [ ] ❌ 비밀정보 하드코딩 금지 (API 키, 비밀번호, 토큰)
- [ ] ❌ .env 파일 커밋 금지
- [ ] ❌ SQL 직접 문자열 조합 금지 (SQL Injection)
- [ ] ❌ 사용자 입력 그대로 출력 금지 (XSS)

### 5.2 필수 적용

- [x] 모든 사용자 입력 검증 (Pydantic 서버 측)
- [x] 비밀번호 해싱 (bcrypt)
- [x] JWT 토큰 인증
- [x] CORS 설정
- [x] 민감 API는 인증된 요청만 접근

### 5.3 환경 변수 관리

```bash
# .env.example (Git 커밋 O)
DATABASE_URL=postgresql://user:password@localhost:5432/asset_status
JWT_SECRET=your-jwt-secret-key-here
OPENAI_API_KEY=your-openai-api-key-here

# .env (Git 커밋 X, .gitignore에 추가 필수)
DATABASE_URL=postgresql://realuser:realpass@localhost:5432/asset_status
JWT_SECRET=abc123xyz789real
OPENAI_API_KEY=sk-...
```

**.gitignore:**
```
.env
__pycache__/
node_modules/
*.pyc
.pytest_cache/
```

---

## 6. 테스트 워크플로우

### 6.1 즉시 실행 검증

코드 작성 후 바로 테스트:

```bash
# 백엔드 (루트 디렉토리에서)
cd backend
pytest tests/ -v --cov=app

# 프론트엔드
cd frontend
npm run test -- --coverage

# E2E
cd frontend
npx playwright test
```

### 6.2 오류 로그 공유 규칙

오류 발생 시 AI에게 전달할 정보:

1. 전체 에러 메시지
2. 관련 코드 스니펫
3. 재현 단계
4. 이미 시도한 해결책

**예시:**
```
## 에러
pydantic.error_wrappers.ValidationError: 1 validation error for AccountCreate
account_type
  value is not a valid enumeration member (type=type_error.enum)

## 코드
# backend/app/schemas/account.py:L12
account_type: AccountType  # Enum

## 재현
1. POST /accounts
2. body: {"account_type": "INVALID", "name": "Test"}

## 시도한 것
- AccountType Enum 정의 확인 → ISA, PENSION, GENERAL, OVERSEAS만 허용
```

---

## 7. Git 워크플로우

### 7.1 브랜치 전략

```
main          # 프로덕션
├── develop   # 개발 통합
│   ├── feature/accounts-be
│   ├── feature/accounts-fe
│   ├── feature/ai-advice-be
│   └── feature/ai-advice-fe
```

### 7.2 커밋 메시지

```
<type>(<scope>): <subject>

<body>
```

**타입:**
- `feat`: 새 기능
- `fix`: 버그 수정
- `refactor`: 리팩토링
- `docs`: 문서
- `test`: 테스트
- `chore`: 기타 (설정, 의존성)

**예시:**
```
feat(accounts): 계좌 CRUD API 구현

- POST /accounts: 계좌 생성
- GET /accounts: 계좌 목록 조회
- TRD 섹션 8.1 RESTful 규칙 준수
- Database Design의 ACCOUNT 엔티티 구현
- 테스트 커버리지 85%
```

---

## 8. 코드 품질 도구

### 8.1 필수 설정

| 도구 | 프론트엔드 | 백엔드 |
|------|-----------|--------|
| 린터 | ESLint | Ruff |
| 포매터 | Prettier | Black |
| 타입 체크 | TypeScript (tsc) | mypy (선택) |

### 8.2 설정 파일

**프론트엔드 (.eslintrc.json):**
```json
{
  "extends": ["eslint:recommended", "plugin:@typescript-eslint/recommended", "plugin:react/recommended"],
  "rules": {
    "react/react-in-jsx-scope": "off"
  }
}
```

**백엔드 (pyproject.toml):**
```toml
[tool.ruff]
line-length = 100
select = ["E", "F", "W"]

[tool.black]
line-length = 100

[tool.mypy]
python_version = "3.11"
strict = true
```

### 8.3 Pre-commit 훅 (선택)

```bash
# 설치
pip install pre-commit

# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: ruff
        name: Ruff
        entry: ruff check
        language: system
        types: [python]
```

---

## 9. API 계약 패턴

### 9.1 계약 파일 예시

**contracts/accounts.contract.ts:**
```typescript
export interface Account {
  id: string;
  user_id: string;
  account_type: 'ISA' | 'PENSION' | 'GENERAL' | 'OVERSEAS' | 'GOLD';
  name: string;
  created_at: string;
  updated_at: string;
}

export interface AccountCreate {
  account_type: Account['account_type'];
  name: string;
}

export interface GetAccountsResponse {
  data: {
    accounts: Account[];
  };
  meta: {
    total: number;
  };
}
```

### 9.2 백엔드 스키마 동기화

**backend/app/schemas/account.py:**
```python
from enum import Enum
from pydantic import BaseModel
from datetime import datetime

class AccountType(str, Enum):
    ISA = "ISA"
    PENSION = "PENSION"
    GENERAL = "GENERAL"
    OVERSEAS = "OVERSEAS"
    GOLD = "GOLD"

class AccountCreate(BaseModel):
    account_type: AccountType
    name: str

class Account(BaseModel):
    id: str
    user_id: str
    account_type: AccountType
    name: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```

---

## 10. 투자 조언 면책 고지

### 10.1 필수 표시

모든 AI 조언 화면에 다음 면책 고지를 명시:

```
⚠️ 면책 고지

본 AI 투자 조언은 참고용이며, 투자 결정은 사용자 본인의 책임입니다.
AI 조언의 정확도는 보장되지 않으며, 투자 손실에 대한 책임은 사용자에게 있습니다.
```

### 10.2 코드 예시

```jsx
// frontend/src/components/AIAdviceDisclaimer.tsx
export function AIAdviceDisclaimer() {
  return (
    <div className="disclaimer" style={{ background: '#FEF3C7', padding: '12px', borderRadius: '8px', marginBottom: '16px' }}>
      <p style={{ fontSize: '12px', color: '#78350F', margin: 0 }}>
        ⚠️ <strong>면책 고지</strong>: 본 AI 투자 조언은 참고용이며, 투자 결정은 사용자 본인의 책임입니다.
        AI 조언의 정확도는 보장되지 않으며, 투자 손실에 대한 책임은 사용자에게 있습니다.
      </p>
    </div>
  );
}
```

---

## Decision Log 참조

| ID | 항목 | 선택 | 이유 |
|----|------|------|------|
| CC-01 | 프로젝트 구조 | BE/FE 분리 | 병렬 개발, Git Worktree 활용 |
| CC-02 | 린터/포매터 | ESLint+Prettier / Ruff+Black | 표준 도구, 커뮤니티 지원 우수 |
| CC-03 | 계약 공유 | contracts/ 디렉토리 | BE/FE 타입 동기화 |
| CC-04 | 면책 고지 | 모든 AI 조언 화면에 표시 | 법적 리스크 최소화 |
