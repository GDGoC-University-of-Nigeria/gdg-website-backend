
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, declarative_base
# from app.core.config import settings



# engine = create_engine(settings.DATABASE_URL, echo=True, future=True, pool_pre_ping=True )

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()


# def get_db():
   
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

from app.core.config import settings

# use an async engine — DATABASE_URL must start with postgresql+asyncpg://
engine = create_async_engine(settings.DATABASE_URL, echo=True, future=True, pool_pre_ping=True)

# async session factory
AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session