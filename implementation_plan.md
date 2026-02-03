# Implementation Plan - T3.1 Holdings Calculation Logic (Backend)

거래 내역(Transactions)을 바탕으로 현재 보유 주식(Holdings)과 실현 수익(Realized Profit)을 계산하는 로직을 구현합니다.

## User Review Required
> [!IMPORTANT]
> **실현 수익 계산 방식**: FIFO(선입선출) 방식을 사용하여 정확한 실현 손익을 계산합니다.
> **평균 단가**: 이동평균법(Moving Average)을 사용하여 "현재 보유 평단"을 계산합니다.

## Proposed Changes

### Backend
#### [NEW] [app/services/holding_calculator.py](file:///D:/code/ai-trading-system/Asset_Status-phase3-holdings-be/backend/app/services/holding_calculator.py)
- `calculate_holdings(transactions: List[Transaction]) -> List[Holding]`
- Logic:
  - Sort transactions by date.
  - Iterate:
    - BUY: Add qty, update avg_price (Moving Average).
    - SELL: Deduct qty, calculate Realized Profit (based on FIFO logic or Avg Price logic? Tasks.md said FIFO).
      - If FIFO: Need to track "Batches" of Buys.
      - If Moving Average (simpler for MVP): Realized Profit = (Sell Price - Curr Avg Price) * Sell Qty.
      - **Decision**: Use **Moving Average** for Avg Price, and **Moving Average** for Realized Profit (standard in most retail apps like Webull/Robinhood for display). Tax reporting usually uses FIFO, but for "Asset Status" dashboard, Avg Price difference is more intuitive for "Performance".
      - However, `tasks.md` specified **FIFO**. I will provide FIFO implementation for Realized Profit to be precise.
  - Return: List of Holdings (symbol, quantity, avg_price, realized_profit_total).

#### [NEW] [app/schemas/holding.py](file:///D:/code/ai-trading-system/Asset_Status-phase3-holdings-be/backend/app/schemas/holding.py)
- `Holding` Schema

#### [NEW] [app/routes/holdings.py](file:///D:/code/ai-trading-system/Asset_Status-phase3-holdings-be/backend/app/routes/holdings.py)
- `GET /holdings?account_id={id}`

## Verification Plan

### Automated Tests
- `backend/tests/unit/test_holding_calculator.py`
  - Case 1: Buy 10 @ 100 -> Holding 10 @ 100.
  - Case 2: Buy 10 @ 100, Buy 10 @ 200 -> Holding 20 @ 150.
  - Case 3: Buy 10 @ 100, Sell 5 @ 150 -> Holding 5 @ 100, Realized Profit 250.
  - Case 4: Buy 10 @ 100, Buy 10 @ 200, Sell 15 @ 150 (FIFO).
    - Sell 10 @ 100 (Profit 500), Sell 5 @ 200 (Loss 250). Total Profit 250.
    - Remaining Holding: 5 @ 200.
