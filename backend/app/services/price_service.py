import yfinance as yf
import time
from typing import Dict, List, Optional
import asyncio

# Simple In-Memory Cache
# Key: Symbol, Value: (Price, Timestamp)
_price_cache: Dict[str, tuple[float, float]] = {}
CACHE_DURATION = 300 # 5 minutes

async def get_current_price(symbol: str) -> float:
    now = time.time()
    
    # Check Cache
    if symbol in _price_cache:
        price, timestamp = _price_cache[symbol]
        if now - timestamp < CACHE_DURATION:
            return price
            
    # Fetch from yfinance
    # yfinance is blocking, so run in executor
    try:
        ticker = yf.Ticker(symbol)
        # fast_info is faster than history
        # but fast_info keys differ by version? 'last_price' or 'regularMarketPrice'
        # Let's try history for reliability firsg
        # price = ticker.fast_info.last_price
        
        # Use history 1d
        hist = await asyncio.to_thread(ticker.history, period="1d")
        if not hist.empty:
            price = float(hist['Close'].iloc[-1])
            _price_cache[symbol] = (price, now)
            return price
            
        return 0.0
    except Exception as e:
        print(f"Error fetching price for {symbol}: {e}")
        # Return old cache if exists even if expired?
        if symbol in _price_cache:
             return _price_cache[symbol][0]
        return 0.0

async def get_bulk_prices(symbols: List[str]) -> Dict[str, float]:
    results = {}
    for sym in symbols:
        results[sym] = await get_current_price(sym)
    return results
