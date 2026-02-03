import pytest
import asyncio
from typing import AsyncGenerator, Generator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base
from app.core.config import settings
from app.main import app

# Test DB URL (Use a separate DB or same with rollup transaction)
# For simplicity in local dev, we use the same DB but roll back transactions, 
# or use a separate test database. Given pgvector complexity, rollup is preferred for speed.
# However, asyncpg doesn't support nested transactions well with pytest-asyncio in some versions.
# We'll use a separate engine for tests if possible, but here we assume 'asset_status' DB is used.
# Ideally, we should use 'asset_status_test'.

TEST_DATABASE_URL = settings.DATABASE_URL

@pytest.fixture(scope="session")
def event_loop() -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def test_engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    # Drop tables (Optional, or keep for inspection)
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

@pytest.fixture
async def db_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    async_session = sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
        await session.rollback() # Rollback after search test to keep DB clean

@pytest.fixture
async def client(db_session) -> AsyncGenerator[AsyncClient, None]:
    # Dependency override
    from app.db.session import get_db
    app.dependency_overrides[get_db] = lambda: db_session
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
    
    app.dependency_overrides.clear()
