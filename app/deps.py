"""
Dependency injection functions for the GDGoC UNN API.

This module provides reusable dependencies for FastAPI route handlers,
including database session management and user authentication checks.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import Depends, HTTPException, status
from app.db.session import get_db
from app.models.user import User


from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from app.core import security
from app.core.config import settings
from app.crud import user as crud_user

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"/auth/login" # Not actually used for Google Auth but required by FastAPI spec
)

async def get_db_session() -> AsyncSession:
    """
    Async dependency function that provides a database session.
    
    Yields:
        AsyncSession: An async SQLAlchemy database session
    """
    async for session in get_db():
        yield session

async def get_current_user(
    db: AsyncSession = Depends(get_db_session),
    token: str = Depends(reusable_oauth2)
) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = payload.get("sub")
        if token_data is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials",
            )
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    
    # Check by ID (since sub is user.id in auth.py)
    result = await db.execute(select(User).filter(User.id == token_data))
    user = result.scalars().first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user