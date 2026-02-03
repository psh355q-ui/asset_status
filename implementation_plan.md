# Implementation Plan - T4.1 AI Advice Generation Logic (Backend)

Google Gemini API(`gemini-2.0-flash`)를 사용하여 사용자의 보유 자산 및 시장 데이터(뉴스 등)를 분석하고 투자 조언을 생성합니다.

## User Review Required
> [!IMPORTANT]
> **사용 모델**: `gemini-2.5-flash` (사용자 지정 모델)
> **데이터 소스**: `yfinance`를 통한 최신 뉴스 및 가격 정보 + 사용자의 현재 `Holdings` 정보.
> **프롬프트 전략**: 투자 성향(추후 확장) 및 현재 시장 상황을 고려한 구체적인 Action(BUY/SELL/HOLD) 제안.

## Proposed Changes

### Backend
#### [NEW] [app/services/ai_advisor.py](file:///D:/code/ai-trading-system/Asset_Status-phase4-ai-be/backend/app/services/ai_advisor.py)
- `generate_advice(user_id: UUID, symbol: str) -> AIAdvice`
- Logic:
  1. Fetch user's holdings for `symbol`.
  2. Fetch recent news and price data for `symbol` via `yfinance`.
  3. Construct prompt with context.
  4. Call Gemini API.
  5. Parse JSON response.
  6. Store in `AI_ADVICE` table.

#### [NEW] [app/schemas/ai_advice.py](file:///D:/code/ai-trading-system/Asset_Status-phase4-ai-be/backend/app/schemas/ai_advice.py)
- `AIAdvice` schema: `recommendation`, `summary`, `details`, `confidence`, `symbol`.

#### [NEW] [app/routes/ai_advice.py](file:///D:/code/ai-trading-system/Asset_Status-phase4-ai-be/backend/app/routes/ai_advice.py)
- `POST /ai-advice/generate` -> Trigger generation.
- `GET /ai-advice/history` -> List previous advices.

#### [NEW] [app/models/ai_advice.py](file:///D:/code/ai-trading-system/Asset_Status-phase4-ai-be/backend/app/models/ai_advice.py)
- `AIAdvice` SQLAlchemy model.

## Verification Plan

### Automated Tests
- `backend/tests/integration/test_ai_advisor.py`
  - Mock Gemini API response.
  - Verify data extraction and DB storage.

### Manual Verification
- Swagger UI를 통해 특정 종목에 대한 AI 조언 생성이 정상 작동하고 DB에 저장되는지 확인.
