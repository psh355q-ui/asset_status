import pytest
from datetime import date, timedelta
from app.services.holding_calculator import calculate_holdings
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionType, Market

# Mock Transaction class if needed, or use simple objects
class MockTransaction:
    def __init__(self, symbol, type, quantity, price, trade_date, market="KR"):
        self.symbol = symbol
        self.type = type
        self.quantity = float(quantity)
        self.price = float(price)
        self.trade_date = trade_date
        self.market = market

def test_calculate_simple_buy():
    txs = [
        MockTransaction("005930", TransactionType.BUY, 10, 70000, date(2024, 1, 1))
    ]
    holdings = calculate_holdings(txs)
    assert len(holdings) == 1
    assert holdings[0].symbol == "005930"
    assert holdings[0].quantity == 10
    assert holdings[0].avg_price == 70000

def test_calculate_average_price_buy_buy():
    txs = [
        MockTransaction("005930", TransactionType.BUY, 10, 60000, date(2024, 1, 1)),
        MockTransaction("005930", TransactionType.BUY, 10, 80000, date(2024, 1, 2))
    ]
    holdings = calculate_holdings(txs)
    assert len(holdings) == 1
    assert holdings[0].quantity == 20
    assert holdings[0].avg_price == 70000 # (600k + 800k) / 20 = 70k

def test_calculate_sell_fifo_profit():
    # Buy 10 @ 100
    # Sell 5 @ 150 -> Realized: (150-100)*5 = 250
    # Remaining: 5 @ 100
    txs = [
        MockTransaction("AAPL", TransactionType.BUY, 10, 100, date(2024, 1, 1), market="US"),
        MockTransaction("AAPL", TransactionType.SELL, 5, 150, date(2024, 1, 2), market="US")
    ]
    holdings = calculate_holdings(txs)
    assert len(holdings) == 1
    assert holdings[0].symbol == "AAPL"
    assert holdings[0].quantity == 5
    assert holdings[0].avg_price == 100
    assert holdings[0].total_realized_profit == 250

def test_calculate_sell_fifo_mixed_batches():
    # Buy 10 @ 100 (Batch A)
    # Buy 10 @ 200 (Batch B). Avg Price now 150.
    # Sell 15 @ 150.
    # FIFO:
    # 1. Sell 10 from A @ 150. Profit: (150-100)*10 = 500. A empty.
    # 2. Sell 5 from B @ 150. Profit: (150-200)*5 = -250. B has 5 left.
    # Total Realized: 250.
    # Remaining: 5 from B @ 200.
    
    txs = [
        MockTransaction("ABC", TransactionType.BUY, 10, 100, date(2024, 1, 1)),
        MockTransaction("ABC", TransactionType.BUY, 10, 200, date(2024, 1, 2)),
        MockTransaction("ABC", TransactionType.SELL, 15, 150, date(2024, 1, 3))
    ]
    holdings = calculate_holdings(txs)
    
    assert holdings[0].quantity == 5
    # Avg price should be remaining batch price (200) not weighted avg of historic? 
    # Usually apps show weighted avg of *remaining*. 
    # If we use strict FIFO for avg price display: Remaining is only from Batch B, so 200.
    assert holdings[0].avg_price == 200 
    assert holdings[0].total_realized_profit == 250

def test_multiple_symbols():
    txs = [
        MockTransaction("A", TransactionType.BUY, 10, 100, date(2024, 1, 1)),
        MockTransaction("B", TransactionType.BUY, 5, 50, date(2024, 1, 1))
    ]
    holdings = calculate_holdings(txs)
    assert len(holdings) == 2
