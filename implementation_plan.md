# Implementation Plan - T2.1 Account Management API (Backend)

Phase 2의 첫 번째 단계인 계좌(Account) 관리 API를 구현합니다.
사용자는 다수의 계좌를 등록하고 관리할 수 있어야 합니다.

## Goal Description
- **API**: `/accounts` 엔드포인트 구현 (CRUD)
- **Security**: 로그인한 사용자(JWT)만 본인의 계좌에 접근 가능 (Row Level Security 구현)
- **Validation**: 계좌명 필수, 통화 코드(KRW/USD) 검증

## User Review Required
> [!IMPORTANT]
> - 초기 잔액은 계좌 생성 시 설정 가능합니다.
> - 계좌 타입(ISA, CMA, 일반 등)은 문자열로 처리하거나 Enum으로 제한할 수 있습니다. (Contracts에 따름)

## Proposed Changes

### Backend
#### [NEW] [schemas/account.py](file:///D:/code/ai-trading-system/Asset_Status-phase2-account-be/backend/app/schemas/account.py)
- `AccountCreate`, `AccountUpdate`, `AccountResponse` Pydantic 모델 정의
- API Contract (`contracts/accounts.contract.ts`) 준수

#### [NEW] [services/account_service.py](file:///D:/code/ai-trading-system/Asset_Status-phase2-account-be/backend/app/services/account_service.py)
- `create_account(user_id, account_in)`: 소유자 할당 후 생성
- `get_accounts(user_id)`: 본인 계좌 목록 조회
- `get_account(user_id, account_id)`: 본인 계좌 상세 조회 (타인 계좌 조회 불가 확인)
- `update_account(user_id, account_id, account_in)`
- `delete_account(user_id, account_id)`

#### [NEW] [routes/accounts.py](file:///D:/code/ai-trading-system/Asset_Status-phase2-account-be/backend/app/routes/accounts.py)
- FastAPI Router 구현
- `Depends(get_current_user)`를 통해 인증 및 `user_id` 확보

#### [MODIFY] [main.py](file:///D:/code/ai-trading-system/Asset_Status-phase2-account-be/backend/app/main.py)
- `/accounts` 라우터 등록

## Verification Plan

### Automated Tests
- **Integration Test**: `backend/tests/integration/test_accounts.py`
  - `test_create_account`: 정상 생성 확인
  - `test_get_accounts`: 목록 조회 및 데이터 검증
  - `test_get_account_detail`: 상세 조회
  - `test_get_others_account`: 타인 계좌 접근 시 404/403 확인 (보안 필수)
  - `test_update_account`: 수정 확인
  - `test_delete_account`: 삭제 확인
