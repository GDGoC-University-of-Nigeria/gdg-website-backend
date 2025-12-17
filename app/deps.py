"""
Dependency injection functions for the GDGoC UNN API.

This module provides reusable dependencies for FastAPI route handlers,
including database session management and user authentication checks.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from app.db.session import get_db
from app.models.user import User


async def get_current_active_user(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(lambda: None)  # Placeholder until auth is implemented
):
    """
    Dependency to get the current authenticated and active user.
    
    Args:
        db: Database session
        current_user: Current authenticated user (from auth middleware)
        
    Returns:
        User: The current active user
        
    Raises:
        HTTPException: If the user is inactive
        
    Note:
        This function requires authentication middleware to be implemented.
        The get_current_user dependency should be created in the auth module.
    """
    if current_user and not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )
    return current_user


async def get_db_session() -> AsyncSession:
    """
    Async dependency function that provides a database session.
    
    Yields:
        AsyncSession: An async SQLAlchemy database session
        
    Usage:
        @app.get("/users")
        async def get_users(db: AsyncSession = Depends(get_db_session)):
            result = await db.execute(select(User))
            return result.scalars().all()
    """
    db = await get_db()
    try:
        yield db
    finally:
        await db.close()