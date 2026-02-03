from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

class AIAdviceBase(BaseModel):
    symbol: str
    recommendation: str
    summary: str
    details: str
    confidence: float

class AIAdviceCreate(AIAdviceBase):
    pass

class AIAdvice(AIAdviceBase):
    id: UUID
    user_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
