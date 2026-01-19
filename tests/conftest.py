"""
Shared test fixtures and configuration.

This module provides reusable fixtures for testing the GDG Backend API.
"""
import pytest
import asyncio
from typing import AsyncGenerator, Generator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool
from faker import Faker
import uuid

from app.main import app
from app.db.session import get_db
from app.db.base import Base
from app.models.user import User
from app.core.security import hash_password, create_access_token
from app.core.config import settings

# Initialize Faker
fake = Faker()


# Database fixtures
@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def test_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Create a test database session.
    
    This fixture creates a new database session for each test and rolls back
    all changes after the test completes to maintain test isolation.
    """
    # Create async engine for testing
    engine = create_async_engine(
        settings.DATABASE_URL,
        poolclass=NullPool,
        echo=False,
    )
    
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Create session
    async_session = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session() as session:
        async with session.begin():
            yield session
            await session.rollback()
    
    # Drop tables after test
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    await engine.dispose()


@pytest.fixture
async def test_client(test_db: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """
    Create a test client for making requests to the API.
    
    This fixture overrides the database dependency to use the test database.
    """
    async def override_get_db():
        yield test_db
    
    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        yield client
    
    app.dependency_overrides.clear()


# User fixtures
@pytest.fixture
async def admin_user(test_db: AsyncSession) -> User:
    """Create an admin user for testing."""
    user = User(
        id=uuid.uuid4(),
        full_name=fake.name(),
        email=fake.email(),
        phone=fake.phone_number()[:15],
        hashed_password=hash_password("testpassword123"),
        is_admin=True,
        provider="local",
        provider_user_id=str(uuid.uuid4()),
    )
    test_db.add(user)
    await test_db.commit()
    await test_db.refresh(user)
    return user


@pytest.fixture
async def regular_user(test_db: AsyncSession) -> User:
    """Create a regular (non-admin) user for testing."""
    user = User(
        id=uuid.uuid4(),
        full_name=fake.name(),
        email=fake.email(),
        phone=fake.phone_number()[:15],
        hashed_password=hash_password("testpassword123"),
        is_admin=False,
        provider="local",
        provider_user_id=str(uuid.uuid4()),
    )
    test_db.add(user)
    await test_db.commit()
    await test_db.refresh(user)
    return user


@pytest.fixture
def admin_headers(admin_user: User) -> dict:
    """Create authentication headers for admin user."""
    access_token = create_access_token(data={"sub": str(admin_user.id)})
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def regular_user_headers(regular_user: User) -> dict:
    """Create authentication headers for regular user."""
    access_token = create_access_token(data={"sub": str(regular_user.id)})
    return {"Authorization": f"Bearer {access_token}"}


# Event data fixtures
@pytest.fixture
def sample_event_data() -> dict:
    """Generate sample event data for testing."""
    return {
        "title": fake.sentence(nb_words=4),
        "description": fake.text(max_nb_chars=200),
        "date": fake.date_between(start_date="today", end_date="+30d").isoformat(),
        "start_time": "14:00:00",
        "end_time": "16:00:00",
        "image_url": fake.image_url(),
        "location": fake.address(),
    }


@pytest.fixture
def sample_event_update_data() -> dict:
    """Generate sample event update data for testing."""
    return {
        "title": fake.sentence(nb_words=4),
        "description": fake.text(max_nb_chars=200),
    }
