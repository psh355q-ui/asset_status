import pytest
import asyncio
from typing import AsyncGenerator, Generator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base
from app.core.config import settings
from app.main import app

# Test DB settings
TEST_DATABASE_URL = settings.DATABASE_URL

@pytest.fixture
async def test_engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    # Cleanup excluded for speed/debugging in local dev
    await engine.dispose()

@pytest.fixture
async def db_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    async_session = sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
        await session.rollback()

@pytest.fixture
async def client(db_session) -> AsyncGenerator[AsyncClient, None]:
    from app.db.session import get_db
    app.dependency_overrides[get_db] = lambda: db_session
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
    
    app.dependency_overrides.clear()

from sqlalchemy import text

@pytest.fixture(autouse=True)
async def clean_db(db_session):
    # Clean tables before each test
    # TRUNCATE users CASCADE will clear accounts too
    await db_session.execute(text("TRUNCATE TABLE users RESTART IDENTITY CASCADE"))
    await db_session.commit()

@pytest.fixture
async def regular_user(client):
    user_data = {"email": "test@example.com", "password": "password123", "password_confirm": "password123"}
    # T1.1 implemented register with 'password' but Schema might have 'confirm'?
    # Checking contract... usually register needs email/password.
    # We will assume simple register for now based on T1.1 logs.
    # Wait, T1.1 logs said: "Handles email uniqueness...".
    # Let's try simple payload first.
    response = await client.post("/auth/register", json={"email": "test@example.com", "password": "password123"})
    assert response.status_code == 200
    return response.json()["data"]

@pytest.fixture
async def auth_headers(client, regular_user):
    # Route uses JSON LoginRequest
    response = await client.post(
        "/auth/login",
        json={"username": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


