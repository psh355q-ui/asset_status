# Implementation Plan - T5.1 E2E Testing (Playwright)

주요 사용자 플로우를 E2E 테스트로 자동화하여 전체 시스템의 안정성을 검증합니다.

## User Review Required
> [!IMPORTANT]
> **테스트 범위**: 회원가입부터 AI 조언 조회까지 전체 플로우를 커버합니다.
> **도구**: Playwright를 사용하여 크로스 브라우저 테스트를 지원합니다.
> **실행 환경**: 로컬 개발 서버(backend + frontend)가 실행 중이어야 합니다.

## Proposed Changes

### Frontend E2E Tests
#### [NEW] [frontend/e2e/auth.spec.ts](file:///D:/code/ai-trading-system/Asset_Status-phase5-e2e/frontend/e2e/auth.spec.ts)
- 회원가입 플로우 테스트
- 로그인/로그아웃 테스트
- 인증 토큰 유지 확인

#### [NEW] [frontend/e2e/accounts.spec.ts](file:///D:/code/ai-trading-system/Asset_Status-phase5-e2e/frontend/e2e/accounts.spec.ts)
- 계좌 생성 테스트
- 계좌 목록 조회 테스트
- 계좌별 거래 입력 테스트

#### [NEW] [frontend/e2e/holdings.spec.ts](file:///D:/code/ai-trading-system/Asset_Status-phase5-e2e/frontend/e2e/holdings.spec.ts)
- 자산 현황 대시보드 렌더링 테스트
- 보유 자산 테이블 데이터 확인
- 차트 표시 확인

#### [NEW] [frontend/e2e/ai-advice.spec.ts](file:///D:/code/ai-trading-system/Asset_Status-phase5-e2e/frontend/e2e/ai-advice.spec.ts)
- AI 조언 페이지 접근 테스트
- 새로운 조언 요청 플로우
- 조언 히스토리 확인

#### [NEW] [playwright.config.ts](file:///D:/code/ai-trading-system/Asset_Status-phase5-e2e/frontend/playwright.config.ts)
- Playwright 설정 파일
- 베이스 URL, 타임아웃, 브라우저 설정

## Verification Plan

### Setup
```bash
cd frontend
npm install -D @playwright/test
npx playwright install
```

### Test Execution
```bash
# 모든 E2E 테스트 실행
npx playwright test

# 특정 테스트만 실행
npx playwright test e2e/auth.spec.ts

# UI 모드로 실행
npx playwright test --ui
```

### Expected Results
- 모든 E2E 테스트가 통과해야 합니다.
- 테스트 실행 시간은 전체 5분 이내여야 합니다.
- 스크린샷/비디오 캡처로 실패 시 디버깅 가능해야 합니다.
