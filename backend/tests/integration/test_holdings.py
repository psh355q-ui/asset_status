import pytest
from httpx import AsyncClient
from datetime import date

@pytest.mark.asyncio
async def test_get_holdings(client: AsyncClient, auth_headers, test_account):
    # Setup: Buy 10 Samsung
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
    
    # Setup: Buy 10 Samsung more @ 80000
    await client.post(
        "/transactions", 
        json={
            "account_id": test_account["id"], 
            "symbol": "005930", 
            "market": "KR", 
            "type": "BUY", 
            "quantity": 10, 
            "price": 80000, 
            "trade_date": str(date.today())
        }, 
        headers=auth_headers
    )

    # Get Holdings
    response = await client.get(f"/holdings?account_id={test_account['id']}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()["data"]
    
    assert len(data) == 1
    item = data[0]
    assert item["symbol"] == "005930"
    assert item["quantity"] == 20
    assert item["avg_price"] == 75000
    assert item["total_realized_profit"] == 0
