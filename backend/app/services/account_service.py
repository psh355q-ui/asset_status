from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.account import Account
from app.schemas.account import AccountCreate, AccountUpdate

async def create_account(db: AsyncSession, user_id: UUID, account_in: AccountCreate) -> Account:
    db_account = Account(
        user_id=user_id,
        name=account_in.name,
        account_type=account_in.account_type
        # balance default 0
    )
    db.add(db_account)
    await db.commit()
    await db.refresh(db_account)
    return db_account

async def get_accounts(db: AsyncSession, user_id: UUID) -> List[Account]:
    result = await db.execute(select(Account).where(Account.user_id == user_id))
    return result.scalars().all()

async def get_account(db: AsyncSession, user_id: UUID, account_id: UUID) -> Optional[Account]:
    result = await db.execute(select(Account).where(Account.id == account_id, Account.user_id == user_id))
    return result.scalars().first()

async def update_account(db: AsyncSession, user_id: UUID, account_id: UUID, account_in: AccountUpdate) -> Optional[Account]:
    account = await get_account(db, user_id, account_id)
    if not account:
        return None
    
    if account_in.name is not None:
        account.name = account_in.name
    
    await db.commit()
    await db.refresh(account)
    return account

async def delete_account(db: AsyncSession, user_id: UUID, account_id: UUID) -> bool:
    account = await get_account(db, user_id, account_id)
    if not account:
        return False
    
    await db.delete(account)
    await db.commit()
    return True
