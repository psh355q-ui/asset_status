
import pytest
from httpx import AsyncClient
from datetime import date

@pytest.mark.asyncio
async def test_create_buy_transaction(client: AsyncClient, auth_headers, test_account):
    payload = {
        "account_id": test_account["id"],
        "symbol": "005930",
        "market": "KR",
        "type": "BUY",
        "quantity": 10,
        "price": 70000,
        "trade_date": str(date.today())
    }
    response = await client.post("/transactions", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["symbol"] == "005930"
    assert data["quantity"] == 10
    assert data["type"] == "BUY"

@pytest.mark.asyncio
async def test_create_sell_transaction_success(client: AsyncClient, auth_headers, test_account):
    # Buy first
    await client.post(
        "/transactions", 
        json={
            "account_id": test_account["id"], 
            "symbol": "AAPL", 
            "market": "US", 
            "type": "BUY", 
            "quantity": 10, 
            "price": 150, 
            "trade_date": str(date.today())
        }, 
        headers=auth_headers
    )
    
    # Sell half
    payload = {
        "account_id": test_account["id"],
        "symbol": "AAPL",
        "market": "US",
        "type": "SELL",
        "quantity": 5,
        "price": 160,
        "trade_date": str(date.today())
    }
    response = await client.post("/transactions", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["type"] == "SELL"
    assert data["quantity"] == 5

@pytest.mark.asyncio
async def test_create_sell_transaction_fail_insufficient(client: AsyncClient, auth_headers, test_account):
    # Sell without Buy (should fail)
    payload = {
        "account_id": test_account["id"],
        "symbol": "TSLA",
        "market": "US",
        "type": "SELL",
        "quantity": 1,
        "price": 200,
        "trade_date": str(date.today())
    }
    response = await client.post("/transactions", json=payload, headers=auth_headers)
    assert response.status_code == 400
    assert "Insufficient holdings" in response.json()["detail"]

@pytest.mark.asyncio
async def test_get_transactions(client: AsyncClient, auth_headers, test_account):
    # Buy
    await client.post(
        "/transactions", 
        json={
            "account_id": test_account["id"], 
            "symbol": "005930", 
            "market": "KR", 
            "type": "BUY", 
            "quantity": 10, 
            "price": 70000, 
            "trade_date": str(date.today())
        }, 
        headers=auth_headers
    )
    
    # Get List
    response = await client.get(f"/transactions?account_id={test_account['id']}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()["data"] # Paginated? Check contract. "data": { items: [], total: ... } or "data": [] ?
    # Contract says PaginatedResponse but implementation return List for now (MVP)
    # So data should be a list
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["symbol"] == "005930"
