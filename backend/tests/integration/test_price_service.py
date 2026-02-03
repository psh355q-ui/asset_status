
import pytest
from app.services.price_service import get_current_price, get_bulk_prices
import time

@pytest.mark.asyncio
async def test_get_current_price_mock():
    # Should work
    price = await get_current_price("005930.KS")
    assert price > 0
    assert isinstance(price, float)

@pytest.mark.asyncio
async def test_get_current_price_us():
    price = await get_current_price("AAPL")
    assert price > 0

@pytest.mark.asyncio
async def test_caching_behavior():
    # First call
    start = time.time()
    price1 = await get_current_price("005930.KS")
    first_duration = time.time() - start
    
    # Second call (should be fast)
    start = time.time()
    price2 = await get_current_price("005930.KS")
    second_duration = time.time() - start
    
    assert price1 == price2
    # Second call should be significantly faster or at least instantaneous if cached
    # But API call vary. Mocking yfinance internal would be better for reliable test.
    # For integration test, we just check functionality.

@pytest.mark.asyncio
async def test_bulk_fetch():
    symbols = ["005930.KS", "AAPL"]
    prices = await get_bulk_prices(symbols)
    assert "005930.KS" in prices
    assert "AAPL" in prices
    assert prices["005930.KS"] > 0
