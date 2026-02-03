# Implementation Plan - T2.4 Transaction Input UI (Frontend)

사용자가 주식, ETF 등의 거래 내역을 입력할 수 있는 모달 폼을 구현합니다.
대시보드 또는 계좌 상세 화면에서 접근할 수 있습니다.

## User Review Required
> [!NOTE]
> - **진입점**: 대시보드 상단에 "Add Transaction" 버튼을 배치하여 모달을 띄웁니다.
> - **계좌 선택**: 모달 내부에서 거래할 계좌를 선택할 수 있게 합니다. (계좌 목록 불러오기 필요)
> - **검증**: 수량, 가격은 0보다 커야 합니다. 심볼은 필수입니다.

## Proposed Changes

### Frontend
#### [NEW] [components/transactions/TransactionFormModal.tsx](file:///D:/code/ai-trading-system/Asset_Status-phase2-transaction-fe/frontend/src/components/transactions/TransactionFormModal.tsx)
- 거래 입력 폼 Modal
- Fields:
  - Account (Select)
  - Market (Radio: KR/US)
  - Type (Radio/Select: BUY/SELL/...)
  - Symbol (Input)
  - Quantity (Number Input)
  - Price (Number Input)
  - Date (Date Input, default Today)
- React Hook Form + Zod Validation

#### [NEW] [services/transactionService.ts](file:///D:/code/ai-trading-system/Asset_Status-phase2-transaction-fe/frontend/src/services/transactionService.ts)
- `createTransaction(data)`
- `getTransactions(filters)`

#### [MODIFY] [pages/Dashboard.tsx](file:///D:/code/ai-trading-system/Asset_Status-phase2-transaction-fe/frontend/src/pages/Dashboard.tsx)
- "Add Transaction" 버튼 추가
- 모달 상태 관리 (isOpen)

#### [MODIFY] [store/useTransactionStore.ts](file:///D:/code/ai-trading-system/Asset_Status-phase2-transaction-fe/frontend/src/store/useTransactionStore.ts)
- (New file) Transaction 상태 관리 (Optional, or just Service call directly form Modal)
- Let's use `useAccountStore` to refresh accounts? No, need to refresh transaction list if we display it.
- For now, T2.4 focuses on **Input**. T3.1 will do Holdings calculation.

## Verification Plan

### Automated Tests
- **Component Test**: `frontend/src/__tests__/transactions/TransactionForm.test.tsx`
  - 폼 렌더링 확인
  - 유효성 검사 에러 확인 (필수값 누락, 음수 입력)
  - 제출 시 API 호출 확인 (Mock Service)

### Manual Verification
1. 대시보드 -> "Add Transaction" 클릭 -> 모달 뜸.
2. 입력 -> 저장 -> 성공 메시지. (DB 저장 확인).
