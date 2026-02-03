import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_account(client: AsyncClient, auth_headers):
    payload = {
        "name": "My ISA Account",
        "account_type": "ISA"
    }
    response = await client.post("/accounts", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["name"] == "My ISA Account"
    assert data["account_type"] == "ISA"
    assert "id" in data
    assert "user_id" in data

@pytest.mark.asyncio
async def test_get_accounts(client: AsyncClient, auth_headers):
    # Create an account first
    await client.post("/accounts", json={"name": "Account 1", "account_type": "GENERAL"}, headers=auth_headers)
    
    response = await client.get("/accounts", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()["data"]
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == "Account 1"

@pytest.mark.asyncio
async def test_get_account_detail(client: AsyncClient, auth_headers):
    # Create
    create_res = await client.post("/accounts", json={"name": "Detail Test", "account_type": "PENSION"}, headers=auth_headers)
    account_id = create_res.json()["data"]["id"]
    
    # Get
    response = await client.get(f"/accounts/{account_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["id"] == account_id
    assert data["name"] == "Detail Test"

@pytest.mark.asyncio
async def test_update_account(client: AsyncClient, auth_headers):
    # Create
    create_res = await client.post("/accounts", json={"name": "Old Name", "account_type": "GENERAL"}, headers=auth_headers)
    account_id = create_res.json()["data"]["id"]
    
    # Update
    payload = {"name": "New Name"}
    response = await client.put(f"/accounts/{account_id}", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["name"] == "New Name"

@pytest.mark.asyncio
async def test_delete_account(client: AsyncClient, auth_headers):
    # Create
    create_res = await client.post("/accounts", json={"name": "To Delete", "account_type": "GENERAL"}, headers=auth_headers)
    account_id = create_res.json()["data"]["id"]
    
    # Delete
    response = await client.delete(f"/accounts/{account_id}", headers=auth_headers)
    assert response.status_code == 200
    
    # Verify Gone
    get_res = await client.get(f"/accounts/{account_id}", headers=auth_headers)
    assert get_res.status_code == 404
