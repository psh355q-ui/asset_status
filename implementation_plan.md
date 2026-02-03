# Implementation Plan - T4.3 AI Advice UI (Frontend)

Gemini 2.5 Flash가 제공하는 투자 조언을 사용자가 확인하고, 새로운 조언을 요청할 수 있는 UI를 구현합니다.

## User Review Required
> [!IMPORTANT]
> **디자인**: `AIAdviceCard`는 추천 결과(BUY/SELL/HOLD)를 직관적인 색상과 아이콘으로 강조합니다.
> **요청 방식**: 특정 종목이 선택된 상태에서 "AI 조언 받기" 버튼을 클릭하여 조언을 생성합니다.
> **히스토리**: 과거에 생성된 조언 목록을 대시보드 하단이나 별도 페이지에서 확인할 수 있습니다.

## Proposed Changes

### Frontend
#### [NEW] [src/services/aiAdviceService.ts](file:///D:/code/ai-trading-system/Asset_Status-phase4-fe/frontend/src/services/aiAdviceService.ts)
- `generateAdvice(symbol: string)`: `POST /ai-advice/generate` 호출.
- `getAdviceHistory()`: `GET /ai-advice/history` 호출.

#### [NEW] [src/components/ai-advice/AIAdviceCard.tsx](file:///D:/code/ai-trading-system/Asset_Status-phase4-fe/frontend/src/components/ai-advice/AIAdviceCard.tsx)
- 추천 타입에 따른 테마 색상 적용 (BUY: Red, SELL: Blue, HOLD: Gray).
- 신뢰도(Confidence) 게이지 표시.
- 요약 및 상세 분석 토글.

#### [NEW] [src/pages/AIAdvicePage.tsx](file:///D:/code/ai-trading-system/Asset_Status-phase4-fe/frontend/src/pages/AIAdvicePage.tsx)
- AI 조언 히스토리 리스트.
- 새로운 종목에 대한 조언 요청 폼.

#### [MODIFY] [src/pages/Dashboard.tsx](file:///D:/code/ai-trading-system/Asset_Status-phase4-fe/frontend/src/pages/Dashboard.tsx)
- 대시보드 사이드바 또는 섹션에 AI 조언 바로가기/요약 추가.

## Verification Plan

### Automated Tests
- `src/__tests__/ai-advice/AIAdviceCard.test.tsx`
  - 추천 결과별 렌더링 확인.
  - 상세 내용 토글 동작 확인.

### Manual Verification
1. 대시보드에서 종목 선택 후 "AI 조언 받기" 클릭.
2. 로딩 상태 확인 및 AI 조언 카드 팝업/표시 확인.
3. AI 조언 페이지에서 과거 히스토리가 정상적으로 나열되는지 확인.
