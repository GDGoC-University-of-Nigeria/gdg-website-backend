from fastapi import Depends, HTTPException, status

from app.dependencies.get_current_user import get_current_user


async def require_admin(current_user=Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )
    return current_user

# from fastapi import Depends, HTTPException, status, Request
# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# from sqlalchemy.ext.asyncio import AsyncSession
# from app.core.security import decode_access_token
# from app.db.session import get_db
# from sqlalchemy import select
# from app.models.user import User
# from typing import Optional

# security = HTTPBearer(auto_error=False)  # Don't auto-error, we'll check cookie too

# async def require_admin(
#     request: Request,
#     credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
#     db: AsyncSession = Depends(get_db)
# ):
#     # Try to get token from Authorization header first
#     token = None
#     if credentials:
#         token = credentials.credentials
#         print(f"Token from header: {token[:20]}...")
#     else:
#         # If not in header, try to get from cookie
#         token = request.cookies.get("access_token")
#         if token:
#             print(f"Token from cookie: {token[:20]}...")
    
#     if not token:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Not authenticated - no token provided"
#         )
    
#     try:
#         payload = decode_access_token(token)
#         print(f"Decoded payload: {payload}")
        
#         user_id = payload.get("sub")
        
#         if not user_id:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Invalid token - no user ID"
#             )
        
#         result = await db.execute(select(User).where(User.id == user_id))
#         user = result.scalar_one_or_none()
        
#         if not user:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="User not found"
#             )
        
#         if not user.is_admin:
#             raise HTTPException(
#                 status_code=status.HTTP_403_FORBIDDEN,
#                 detail="Not authorized - admin required"
#             )
        
#         print(f"Admin authenticated: {user.email}")
#         return user
        
#     except HTTPException:
#         raise
#     except Exception as e:
#         print(f"Error in require_admin: {type(e).__name__}: {e}")
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail=f"Token validation failed: {str(e)}"
#         )


