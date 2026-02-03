# Implementation Plan - T2.3 Transaction Management API (Backend)

주식, ETF 등의 거래 내역(매수/매도)을 기록하고 관리하는 API를 구현합니다.
매도(SELL) 시에는 해당 계좌에 충분한 보유 수량이 있는지 검증해야 합니다.

## Goal Description
- **API**: `/transactions` (CRUD)
- **Logic**:
  - `POST /transactions`: 거래 기록 (매수/매도/배당 등)
  - `GET /transactions`: 계좌별, 종목별 필터링 조회
- **Validation**:
  - 기본적인 값 검증 (수량 > 0, 가격 >= 0)
  - **Business Rule**: 매도 시, 해당 계좌의 해당 종목 보유 수량 >= 매도 수량 (Simple Validation)

## User Review Required
> [!NOTE]
> - **보유 수량 계산**: 현재(M2) 단계에서는 `Transaction` 테이블의 합산으로만 계산합니다. (복잡한 배당 재투자나 분할 이슈는 M3/M4에서 다룸)
> - **통화**: 계좌의 통화(KRW/USD)와 거래 통화가 일치한다고 가정합니다. (환전 로직 제외)

## Proposed Changes

### Backend
#### [NEW] [schemas/transaction.py](file:///D:/code/ai-trading-system/Asset_Status-phase2-transaction-be/backend/app/schemas/transaction.py)
- `TransactionCreate`, `TransactionResponse` 정의
- `TransactionType` Enum (BUY, SELL, DIVIDEND, DEPOSIT, WITHDRAW) 사용

#### [NEW] [services/transaction_service.py](file:///D:/code/ai-trading-system/Asset_Status-phase2-transaction-be/backend/app/services/transaction_service.py)
- `create_transaction`:
  - 매도(SELL) 요청 시 `validate_holdings(account_id, symbol, quantity)` 호출
  - DB 저장
- `get_transactions`: 필터링 조회
- `validate_holdings`: 해당 계좌/종목의 (총 매수 - 총 매도) 계산

#### [NEW] [routes/transactions.py](file:///D:/code/ai-trading-system/Asset_Status-phase2-transaction-be/backend/app/routes/transactions.py)
- Router 정의

#### [MODIFY] [models/transaction.py](file:///D:/code/ai-trading-system/Asset_Status-phase2-transaction-be/backend/app/models/transaction.py)
- 모델 필드 확인 및 필요 시 인덱스 추가 (account_id, symbol)

#### [MODIFY] [main.py](file:///D:/code/ai-trading-system/Asset_Status-phase2-transaction-be/backend/app/main.py)
- 라우터 등록

## Verification Plan

### Automated Tests
- **Integration Test**: `backend/tests/integration/test_transactions.py`
  - `test_create_buy`: 매수 성공
  - `test_create_sell_success`: 보유 수량 내 매도 성공
  - `test_create_sell_fail`: 보유 수량 부족 시 에러 (400 Bad Request)
  - `test_get_transactions`: 필터링 동작 확인
