from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services import transaction_service
from app.schemas.transaction import TransactionCreate, TransactionResponse
from app.schemas.auth import ApiResponse
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("", response_model=ApiResponse[TransactionResponse])
async def create_transaction(
    transaction_in: TransactionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    transaction = await transaction_service.create_transaction(db, current_user.id, transaction_in)
    return {"data": transaction}

@router.get("", response_model=ApiResponse[List[TransactionResponse]])
async def get_transactions(
    account_id: Optional[UUID] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    transactions = await transaction_service.get_transactions(db, current_user.id, account_id)
    return {"data": transactions}
