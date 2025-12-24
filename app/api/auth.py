from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from google.oauth2 import id_token
from google.auth.transport import requests
from app.core.config import settings
from app.core.security import create_access_token
from app.deps import get_db_session
from app.schemas.auth import GoogleAuthRequest
from app.schemas.user import UserCreate
from app.crud import user as crud_user

router = APIRouter()

@router.post("/google", status_code=status.HTTP_200_OK)
async def login_google(
    request: GoogleAuthRequest,
    response: Response,
    db: AsyncSession = Depends(get_db_session)
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests using Google ID token.
    """
    try:
        # Verify Google ID Token
        id_info = id_token.verify_oauth2_token(
            request.id_token, 
            requests.Request(), 
            settings.GOOGLE_CLIENT_ID
        )

        email = id_info.get("email")
        google_sub = id_info.get("sub")
        
        if not email:
            raise HTTPException(status_code=400, detail="Email not found in token")

        # Check if user exists
        user = await crud_user.get_by_email(db, email=email)
        
        if not user:
            # Create new user
            user_in = UserCreate(
                email=email,
                provider="google",
                provider_user_id=google_sub,
                full_name=id_info.get("name"),
                avatar_url=id_info.get("picture"),
                profile_complete=False
            )
            user = await crud_user.create_from_google(db, user_in)
        
        # Create access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            subject=str(user.id), expires_delta=access_token_expires
        )
        
        # Set HttpOnly cookie
        response.set_cookie(
            key="access_token",
            value=f"Bearer {access_token}",
            httponly=True,
            secure=True, # Set to True in production (HTTPS)
            samesite="lax",
            max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "profile_complete": user.profile_complete,
            "user": {
                "id": str(user.id),
                "email": user.email,
                "full_name": user.full_name,
                "avatar_url": user.avatar_url,
                "profile_complete": user.profile_complete
            }
        }
        
    except ValueError as e:
        # Invalid token
        raise HTTPException(status_code=401, detail=f"Invalid Google token: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Authentication error: {str(e)}")
