from fastapi import APIRouter, Depends
from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services import transaction_service
from app.services.holding_calculator import calculate_holdings
from app.schemas.holding import Holding
from app.schemas.auth import ApiResponse
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("", response_model=ApiResponse[List[Holding]])
async def get_holdings(
    account_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 1. Get all transactions for the account
    transactions = await transaction_service.get_transactions(db, current_user.id, account_id)
    
    # 2. Calculate holdings
    holdings = await calculate_holdings(transactions)
    
    return {"data": holdings}
