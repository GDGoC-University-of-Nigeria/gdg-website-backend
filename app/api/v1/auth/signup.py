from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.auth.signup import SignUpRequest, UserResponse
from app.services.auth.signup import create_user
from app.db.session import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup", response_model=UserResponse, status_code=201)
def signup(data: SignUpRequest, db: Session = Depends(get_db)):
    try:
        user = create_user(
            db=db,
            email=data.email,
            password=data.password,
            full_name=data.full_name,
            phone=data.phone
        )
        return user
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )
