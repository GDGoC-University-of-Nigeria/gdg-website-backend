from fastapi import APIRouter, Depends, Response, HTTPException
from sqlalchemy.orm import Session

from app.schemas.auth.login import LoginRequest
from app.services.auth.login import authenticate_user
from app.services.auth.tokens import create_access_token, create_refresh_token
from app.db.session import get_db
from app.core.config import settings
router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
def login(
    payload: LoginRequest,
    response: Response,
    db: Session = Depends(get_db),
):
    user = authenticate_user(payload.email, payload.password, db)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(subject=str(user.id))
    refresh_token = create_refresh_token(subject=str(user.id))

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=60 * settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=60 * 60 * 24 * settings.REFRESH_TOKEN_EXPIRE_DAYS,
    )
    return {"message": "Login successful"}
