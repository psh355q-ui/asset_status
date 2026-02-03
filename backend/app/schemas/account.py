from pydantic import BaseModel, ConfigDict
from enum import Enum
from typing import Optional
from datetime import datetime
from uuid import UUID

# ------------- Enums ------------- #

class AccountType(str, Enum):
    ISA = 'ISA'
    PENSION = 'PENSION'
    GENERAL = 'GENERAL'
    OVERSEAS = 'OVERSEAS'
    GOLD = 'GOLD'
    # Add more as needed

# ------------- Schemas ------------- #

class AccountBase(BaseModel):
    name: str
    account_type: AccountType

class AccountCreate(AccountBase):
    pass

class AccountUpdate(BaseModel):
    name: Optional[str] = None
    # account_type usually not changeable? Let's assume name only for now as per contract

class AccountResponse(AccountBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)
