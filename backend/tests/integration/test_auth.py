import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User

# Mock User Data
EMAIL = "test@example.com"
PASSWORD = "password123"

@pytest.mark.asyncio
async def test_register_user(client: AsyncClient, db_session: AsyncSession):
    # 1. Register
    response = await client.post(
        "/auth/register",
        json={"email": EMAIL, "password": PASSWORD}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["email"] == EMAIL
    assert "id" in data["data"]
    assert "password" not in data["data"] # Security check

    # 2. Verify DB
    # (Optional: Direct DB check if needed, but API response check is usually enough for integration)

@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient):
    # Register first time
    await client.post(
        "/auth/register",
        json={"email": "duplicate@example.com", "password": PASSWORD}
    )
    
    # Register second time
    response = await client.post(
        "/auth/register",
        json={"email": "duplicate@example.com", "password": PASSWORD}
    )
    assert response.status_code == 400 # Or 409 Conflict

@pytest.mark.asyncio
async def test_login_user(client: AsyncClient):
    # Register
    await client.post(
        "/auth/register",
        json={"email": "login@example.com", "password": PASSWORD}
    )

    # Login (OAuth2 Password Request Form? Or JSON?)
    # Requirements said "POST /auth/login". Usually logic uses JSON or Form.
    # FastAPIs OAuth2PasswordBearer uses Form. But let's assume JSON for modern SPA if not strictly OAuth2 flow.
    # However, Contracts defined: interface LoginRequest { username, password }.
    # Let's use JSON as per contract.
    
    response = await client.post(
        "/auth/login",
        json={"username": "login@example.com", "password": PASSWORD}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient):
    # Register
    await client.post(
        "/auth/register",
        json={"email": "wrongpass@example.com", "password": PASSWORD}
    )

    # Wrong Password
    response = await client.post(
        "/auth/login",
        json={"username": "wrongpass@example.com", "password": "wrong"}
    )
    assert response.status_code == 401
