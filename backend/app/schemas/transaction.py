from pydantic import BaseModel, ConfigDict, Field, field_validator
from enum import Enum
from typing import Optional, List
from datetime import date, datetime
from uuid import UUID

class TransactionType(str, Enum):
    BUY = 'BUY'
    SELL = 'SELL'
    DIVIDEND = 'DIVIDEND'
    DEPOSIT = 'DEPOSIT'
    WITHDRAW = 'WITHDRAW'

class Market(str, Enum):
    KR = 'KR'
    US = 'US'

class TransactionBase(BaseModel):
    symbol: str
    market: Market
    type: TransactionType
    quantity: float = Field(..., gt=0, description="Quantity must be positive")
    price: float = Field(..., gt=0, description="Price must be positive")
    trade_date: date

class TransactionCreate(TransactionBase):
    account_id: UUID

class TransactionResponse(TransactionBase):
    id: UUID
    user_id: UUID
    account_id: UUID
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
