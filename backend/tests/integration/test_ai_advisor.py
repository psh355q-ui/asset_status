import pytest
from httpx import AsyncClient
from unittest.mock import patch
from app.schemas.ai_advice import AIAdviceCreate

@pytest.mark.asyncio
async def test_generate_ai_advice_success(client: AsyncClient, auth_headers):
    # Mock return value for generate_advice
    mock_advice = AIAdviceCreate(
        symbol="005930.KS",
        recommendation="BUY",
        summary="Strong fundamentals and recent good news.",
        details="Samsung Electronics shows recovered semiconductor demand...",
        confidence=0.85
    )
    
    with patch("app.services.ai_advisor_service.ai_advisor.generate_advice", return_value=mock_advice):
        response = await client.post(
            "/ai-advice/generate",
            json={"symbol": "005930.KS"},
            headers=auth_headers
        )
        
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["recommendation"] == "BUY"
    assert data["symbol"] == "005930.KS"
    assert "id" in data

@pytest.mark.asyncio
async def test_get_ai_advice_history(client: AsyncClient, auth_headers):
    # 1. First generate advice to ensure history is not empty
    mock_advice = AIAdviceCreate(
        symbol="AAPL",
        recommendation="HOLD",
        summary="Maintaining position.",
        details="Apple shows stable performance.",
        confidence=0.9
    )
    with patch("app.services.ai_advisor_service.ai_advisor.generate_advice", return_value=mock_advice):
        await client.post(
            "/ai-advice/generate",
            json={"symbol": "AAPL"},
            headers=auth_headers
        )

    # 2. Then check history
    response = await client.get("/ai-advice/history", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()["data"]
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["symbol"] == "AAPL"
