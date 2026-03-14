# from fastapi import Depends, HTTPException, status
# from sqlalchemy.ext.asyncio import AsyncSession

# from app.core.security import decode_access_token
# from app.db.session import get_db
# from app.repositories.users import get_user_by_id


# async def get_current_user(
#     token: str = Depends(decode_access_token),
#     db: AsyncSession = Depends(get_db),
# ):
#     user_id = token.get("sub")

#     if not user_id:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid authentication token",
#         )

#     user = await get_user_by_id(db, user_id)

#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="User not found",
#         )

#     return user

from typing import Optional
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.config import settings
from app.db.session import get_db
from app.models.user import User


# Make HTTPBearer optional (auto_error=False)
security = HTTPBearer(auto_error=False)


async def get_current_user(
    request: Request,
    db: AsyncSession = Depends(get_db),
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> User:
    """
    Get current user from JWT token.
    Accepts token from either:
    1. Authorization header (Bearer token)
    2. Cookie (access_token)
    """
    
    # Try to get token from header first
    token = None
    if credentials:
        token = credentials.credentials
    
    # If not in header, try cookie
    if not token:
        token = request.cookies.get("access_token")
    
    # If still no token, raise error
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        # Decode JWT token
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )
            
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    
    # Get user from database, ensuring they are still active
    result = await db.execute(select(User).where(User.id == user_id, User.is_active.is_(True)))
    user = result.scalar_one_or_none()
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    
    return user