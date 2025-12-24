"""
Database session management for the GDGoC UNN API.

This module configures the SQLAlchemy database engine and session factory,
providing database connections for the FastAPI application.
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Create database engine using the DATABASE_URL from configuration
# echo=True enables SQL query logging for debugging
# Ensure usage of async driver
db_url = settings.DATABASE_URL
if "postgresql://" in db_url and "asyncpg" not in db_url:
     db_url = db_url.replace("postgresql://", "postgresql+asyncpg://")

engine = create_async_engine(db_url, echo=True, future=True)

# AsyncSessionLocal is a factory for creating database sessions
AsyncSessionLocal = sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False,
    autocommit=False, 
    autoflush=False
)

# Base class for declarative models
Base = declarative_base()


async def get_db():
    """
    Dependency function that provides a database session to route handlers.
    
    Yields:
        AsyncSession: A SQLAlchemy database session
    """
    async with AsyncSessionLocal() as session:
        yield session