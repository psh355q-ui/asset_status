# Implementation Plan - T3.2 Market Price Service (Backend)

외부 API(`yfinance`)를 사용하여 한국 및 미국 주식의 현재가를 조회합니다.
빈번한 API 호출을 방지하기 위해 Simple In-Memory Caching (or Redis if available, but for now simple dictionary)를 사용합니다.

## User Review Required
> [!NOTE]
> **캐싱 전략**: 현재가를 5분(300초) 동안 캐싱합니다.
> **장애 대응**: `yfinance` 에러 시 캐시된 최신 가격을 반환하거나, 없으면 에러를 발생시키는 대신 0 또는 마지막 종가를 반환하도록 처리합니다.

## Proposed Changes

### Backend
#### [NEW] [app/services/price_service.py](file:///D:/code/ai-trading-system/Asset_Status-phase3-prices-be/backend/app/services/price_service.py)
- `get_current_price(symbol: str, market: str) -> float`
  - Check Cache.
  - If miss: `yfinance.Ticker(symbol).history(period='1d')`.
  - Update Cache.
- `get_bulk_prices(symbols: List[str]) -> Dict[str, float]`

#### [MODIFY] [app/services/holding_calculator.py](file:///D:/code/ai-trading-system/Asset_Status-phase3-prices-be/backend/app/services/holding_calculator.py)
- `calculate_holdings` 함수 내에서 `price_service.get_current_price` 호출하여 `current_price` 및 `valuation_profit` 계산 로직 추가.
- (Dependencies: `price_service` 주입 필요).

#### [MODIFY] [app/routes/holdings.py](file:///D:/code/ai-trading-system/Asset_Status-phase3-prices-be/backend/app/routes/holdings.py)
- `get_holdings`에서 `calculate_holdings` 호출 시 가격 정보 통합.

## Verification Plan

### Automated Tests
- `backend/tests/integration/test_price_service.py`
  - `get_current_price("005930.KS")` -> Returns float > 0.
  - `get_current_price("AAPL")` -> Returns float > 0.
  - Test Caching: Call twice, verify 2nd call is fast / doesn't hit API (using Mock).

### Manual Verification
- `/holdings` 호출 시 `current_price`가 채워져 있는지 확인.
