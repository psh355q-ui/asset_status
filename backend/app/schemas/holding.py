from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class Holding(BaseModel):
    symbol: str
    market: str
    quantity: float
    avg_price: float
    current_price: float = 0
    total_value: float = 0
    valuation_profit: float = 0 # Unrealized
    realized_profit: float = 0 # Realized logic might be separate, but let's keep it if we calculate per holding session.
                               # Actually realized profit is usually aggregated over time, not "current holding".
                               # But let's include "cumulative realized profit from this symbol" if possible, or just ignore for now.
    
    # For now, let's stick to Current Status. Realized Profit is usually a separate report.
    # But Task T3.1 says "실현 수익 계산". 
    # Let's add `total_realized_profit` field.
    total_realized_profit: float = 0

class Portfolio(BaseModel):
    holdings: List[Holding]
    total_asset_value: float
    total_profit: float
    total_realized_profit: float
