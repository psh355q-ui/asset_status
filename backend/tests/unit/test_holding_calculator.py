
import pytest
import unittest.mock
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

@pytest.mark.asyncio
async def test_calculate_simple_buy():
    txs = [
        MockTransaction("005930.KS", TransactionType.BUY, 10, 70000, date(2024, 1, 1))
    ]
    # We need to mock price_service.get_current_price because calculate_holdings calls it.
    with unittest.mock.patch("app.services.price_service.get_current_price", return_value=75000):
        holdings = await calculate_holdings(txs)
    
    assert len(holdings) == 1
    assert holdings[0].symbol == "005930.KS"
    assert holdings[0].quantity == 10
    assert holdings[0].avg_price == 70000
    assert holdings[0].current_price == 75000
    assert holdings[0].valuation_profit == 50000

@pytest.mark.asyncio
async def test_calculate_average_price_buy_buy():
    txs = [
        MockTransaction("005930", TransactionType.BUY, 10, 60000, date(2024, 1, 1)),
        MockTransaction("005930", TransactionType.BUY, 10, 80000, date(2024, 1, 2))
    ]
    with unittest.mock.patch("app.services.price_service.get_current_price", return_value=70000):
        holdings = await calculate_holdings(txs)
    assert len(holdings) == 1
    assert holdings[0].quantity == 20
    assert holdings[0].avg_price == 70000 

@pytest.mark.asyncio
async def test_calculate_sell_fifo_profit():
    txs = [
        MockTransaction("AAPL", TransactionType.BUY, 10, 100, date(2024, 1, 1), market="US"),
        MockTransaction("AAPL", TransactionType.SELL, 5, 150, date(2024, 1, 2), market="US")
    ]
    with unittest.mock.patch("app.services.price_service.get_current_price", return_value=160):
        holdings = await calculate_holdings(txs)
    assert len(holdings) == 1
    assert holdings[0].symbol == "AAPL"
    assert holdings[0].quantity == 5
    assert holdings[0].avg_price == 100
    assert holdings[0].total_realized_profit == 250

@pytest.mark.asyncio
async def test_calculate_sell_fifo_mixed_batches():
    txs = [
        MockTransaction("ABC", TransactionType.BUY, 10, 100, date(2024, 1, 1)),
        MockTransaction("ABC", TransactionType.BUY, 10, 200, date(2024, 1, 2)),
        MockTransaction("ABC", TransactionType.SELL, 15, 150, date(2024, 1, 3))
    ]
    with unittest.mock.patch("app.services.price_service.get_current_price", return_value=200):
        holdings = await calculate_holdings(txs)
    
    assert holdings[0].quantity == 5
    assert holdings[0].avg_price == 200 
    assert holdings[0].total_realized_profit == 250

@pytest.mark.asyncio
async def test_multiple_symbols():
    txs = [
        MockTransaction("A", TransactionType.BUY, 10, 100, date(2024, 1, 1)),
        MockTransaction("B", TransactionType.BUY, 5, 50, date(2024, 1, 1))
    ]
    
    # Mock return value based on arg
    async def mock_get_price(symbol):
        return 120 if symbol == "A" else 60
        
    with unittest.mock.patch("app.services.price_service.get_current_price", side_effect=mock_get_price):
        holdings = await calculate_holdings(txs)
        
    assert len(holdings) == 2
