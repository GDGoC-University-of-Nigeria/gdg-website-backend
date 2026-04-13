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
    Priority:
      1. Authorization header (Bearer token) — always takes precedence
      2. access_token cookie — fallback for browser-based sessions
    """
    token: Optional[str] = None

    # 1. Authorization header takes priority
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ", 1)[1]
    else:
        # 2. Fall back to cookie
        token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
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
    from sqlalchemy.orm import selectinload
    stmt = select(User).options(selectinload(User.profile)).where(User.id == user_id, User.is_active.is_(True))
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if user is None:
        # Check if the user exists but is inactive
        check_stmt = select(User).where(User.id == user_id)
        check_res = await db.execute(check_stmt)
        exists = check_res.scalar_one_or_none()
        
        if exists:
            import logging
            logging.getLogger("app.auth").warning(f"Auth failed: User {user_id} exists but is_active=False")
            
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )

    return user