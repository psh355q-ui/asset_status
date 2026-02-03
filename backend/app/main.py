from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, accounts, transactions, holdings, ai_advice

app = FastAPI(title="API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(accounts.router, prefix="/accounts", tags=["accounts"])
app.include_router(transactions.router, prefix="/transactions", tags=["transactions"])
app.include_router(holdings.router, prefix="/holdings", tags=["holdings"])
app.include_router(ai_advice.router, prefix="/ai-advice", tags=["ai-advice"])

@app.get("/health")
async def health_check():
    return {"status": "ok"}
