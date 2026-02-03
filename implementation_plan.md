# Implementation Plan - T2.2 Account Management UI (Frontend)

계좌 목록을 조회하고 새로운 계좌를 추가할 수 있는 UI를 구현합니다.
기존 Dashboard 페이지를 확장하여 계좌 관리 기능을 통합합니다.

## User Review Required
> [!NOTE]
> - **디자인**: 노션 스타일의 깔끔한 카드 디자인을 적용합니다.
> - **계좌 생성**: 별도 페이지 이동 없이 모달(Modal) 또는 인라인 폼으로 처리하여 UX를 향상시킵니다. (MVP는 모달 권장)
> - **초기 데이터**: 계좌가 없을 경우 "첫 계좌를 개설해보세요"와 같은 CTA(Call To Action)를 표시합니다.

## Proposed Changes

### Frontend
#### [NEW] [components/accounts/AccountCard.tsx](file:///D:/code/ai-trading-system/Asset_Status-phase2-account-fe/frontend/src/components/accounts/AccountCard.tsx)
- 개별 계좌 정보를 보여주는 카드 컴포넌트
- 계좌명, 타입, 잔액(초기 0원), 아이콘 표시

#### [NEW] [components/accounts/CreateAccountModal.tsx](file:///D:/code/ai-trading-system/Asset_Status-phase2-account-fe/frontend/src/components/accounts/CreateAccountModal.tsx)
- 계좌 생성 폼 (계좌명, 타입 선택)
- React Hook Form + Zod 사용

#### [NEW] [services/accountService.ts](file:///D:/code/ai-trading-system/Asset_Status-phase2-account-fe/frontend/src/services/accountService.ts)
- `getAccounts()`: GET /accounts
- `createAccount(data)`: POST /accounts
- `deleteAccount(id)`: DELETE /accounts/{id}

#### [NEW] [store/useAccountStore.ts](file:///D:/code/ai-trading-system/Asset_Status-phase2-account-fe/frontend/src/store/useAccountStore.ts)
- Zustand 스토어
- `accounts`: Account[]
- `fetchAccounts()`: Thunk action

#### [MODIFY] [pages/Dashboard.tsx](file:///D:/code/ai-trading-system/Asset_Status-phase2-account-fe/frontend/src/pages/Dashboard.tsx)
- 계좌 목록 섹션 추가
- `useAccountStore` 연결
- "계좌 추가" 버튼 및 모달 연동

## Verification Plan

### Automated Tests
- **Component Test**: `frontend/src/__tests__/accounts/AccountCard.test.tsx` (using React Testing Library)
- **Store Test**: Mock Service를 사용하여 Zustand 액션 테스트

### Manual Verification
1. 로그인 후 Dashboard 진입 시 계좌 목록 로딩 확인.
2. "계좌 추가" 클릭 -> 모달 팝업 -> 입력 -> 저장 -> 목록 갱신 확인.
3. 생성된 계좌가 백엔드 DB에 저장되었는지 확인.
