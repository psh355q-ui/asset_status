from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.db.session import get_db
from app.schemas.ai_advice import AIAdvice, AIAdviceCreate
from app.schemas.auth import ApiResponse
from app.models.ai_advice import AIAdvice as AIAdviceModel
from app.models.user import User
from app.core.security import get_current_user
from app.services.ai_advisor_service import ai_advisor
from app.services import transaction_service
from app.services.holding_calculator import calculate_holdings

router = APIRouter()

@router.post("/generate", response_model=ApiResponse[AIAdvice])
async def generate_advice(
    params: dict, # {"symbol": "..."}
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    symbol = params.get("symbol")
    if not symbol:
        raise HTTPException(status_code=400, detail="Symbol is required")
    
    # 1. Get user holdings context
    # Simply fetch all transactions for this user/symbol to provide context
    # Instead of account-specific, let's look at all accounts for better AI context?
    # For now, let's keep it simple.
    transactions = await transaction_service.get_transactions(db, current_user.id)
    holdings = await calculate_holdings(transactions)
    target_holding = next((h for h in holdings if h.symbol == symbol), None)
    
    holdings_context = "No current holdings for this stock."
    if target_holding:
        holdings_context = (
            f"Currently holding {target_holding.quantity} shares. "
            f"Average purchase price is {target_holding.avg_price}. "
            f"Currently UNREALIZED profit is {target_holding.valuation_profit}."
        )

    # 2. Generate with Gemini
    try:
        advice_in = await ai_advisor.generate_advice(symbol, holdings_context)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    # 3. Store in DB
    db_advice = AIAdviceModel(
        user_id=current_user.id,
        **advice_in.dict()
    )
    db.add(db_advice)
    await db.commit()
    await db.refresh(db_advice)
    
    return {"data": db_advice}

@router.get("/history", response_model=ApiResponse[List[AIAdvice]])
async def get_history(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(AIAdviceModel)
        .where(AIAdviceModel.user_id == current_user.id)
        .order_by(AIAdviceModel.created_at.desc())
    )
    advices = result.scalars().all()
    return {"data": advices}
