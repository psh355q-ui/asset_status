from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services import account_service
from app.schemas.account import AccountCreate, AccountUpdate, AccountResponse
from app.schemas.auth import ApiResponse
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("", response_model=ApiResponse[AccountResponse])
async def create_account(
    account_in: AccountCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    account = await account_service.create_account(db, current_user.id, account_in)
    return {"data": account}

@router.get("", response_model=ApiResponse[List[AccountResponse]])
async def get_accounts(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    accounts = await account_service.get_accounts(db, current_user.id)
    return {"data": accounts}

@router.get("/{account_id}", response_model=ApiResponse[AccountResponse])
async def get_account(
    account_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    account = await account_service.get_account(db, current_user.id, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"data": account}

@router.put("/{account_id}", response_model=ApiResponse[AccountResponse])
async def update_account(
    account_id: UUID,
    account_in: AccountUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    account = await account_service.update_account(db, current_user.id, account_id, account_in)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"data": account}

@router.delete("/{account_id}", response_model=ApiResponse[dict])
async def delete_account(
    account_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    success = await account_service.delete_account(db, current_user.id, account_id)
    if not success:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"data": {"id": str(account_id)}}
