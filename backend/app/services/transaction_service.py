from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from fastapi import HTTPException
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionType

async def validate_holdings(db: AsyncSession, account_id: UUID, symbol: str, quantity_to_sell: float):
    # Calculate current holding: SUM(BUY) - SUM(SELL)
    stmt = select(
        func.sum(Transaction.quantity).filter(Transaction.type == TransactionType.BUY),
        func.sum(Transaction.quantity).filter(Transaction.type == TransactionType.SELL)
    ).where(Transaction.account_id == account_id, Transaction.symbol == symbol)
    
    result = await db.execute(stmt)
    total_buy, total_sell = result.first()
    
    current_quantity = (total_buy or 0) - (total_sell or 0)
    
    if current_quantity < quantity_to_sell:
        raise HTTPException(
            status_code=400, 
            detail=f"Insufficient holdings. Current: {current_quantity}, Required: {quantity_to_sell}"
        )

async def create_transaction(db: AsyncSession, user_id: UUID, transaction_in: TransactionCreate) -> Transaction:
    # Validate holdings for SELL
    if transaction_in.type == TransactionType.SELL:
        await validate_holdings(db, transaction_in.account_id, transaction_in.symbol, transaction_in.quantity)
        
    db_transaction = Transaction(
        user_id=user_id,
        account_id=transaction_in.account_id,
        symbol=transaction_in.symbol,
        market=transaction_in.market,
        type=transaction_in.type,
        quantity=transaction_in.quantity,
        price=transaction_in.price,
        trade_date=transaction_in.trade_date
    )
    db.add(db_transaction)
    await db.commit()
    await db.refresh(db_transaction)
    return db_transaction

async def get_transactions(
    db: AsyncSession, 
    user_id: UUID, 
    account_id: UUID = None
) -> List[Transaction]:
    query = select(Transaction).where(Transaction.user_id == user_id)
    
    if account_id:
        query = query.where(Transaction.account_id == account_id)
        
    query = query.order_by(Transaction.trade_date.desc(), Transaction.created_at.desc())
    
    result = await db.execute(query)
    return result.scalars().all()
