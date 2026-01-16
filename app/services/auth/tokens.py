# from datetime import datetime, timedelta
# from jose import jwt
# from app.core.config import settings


# SECRET_KEY = settings.SECRET_KEY
# ALGORITHM = settings.ALGORITHM

# ACCESS_TOKEN_EXPIRE_MINS = settings.ACCESS_TOKEN_EXPIRE_MINUTES
# REFRESH_TOKEN_EXPIRE = settings.REFRESH_TOKEN_EXPIRE_DAYS


# def create_access_token(subject: str, expires_delta: timedelta | None = None):
#     expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINS))
#     to_encode = {"sub": subject, "exp": expire}
#     return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# def create_refresh_token(subject: str, expires_delta: timedelta | None = None) -> str:
#     expire = datetime.utcnow() + (expires_delta or timedelta(days=REFRESH_TOKEN_EXPIRE))
#     to_encode = {"sub": subject, "exp": expire, "type": "refresh"}
#     return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

from datetime import datetime, timedelta
from typing import Dict, Any
from jose import jwt
from app.core.config import settings


SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

ACCESS_TOKEN_EXPIRE_MINS = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE = settings.REFRESH_TOKEN_EXPIRE_DAYS


def create_access_token(
    subject: str, 
    additional_claims: Dict[str, Any] | None = None,
    expires_delta: timedelta | None = None
):
    """Create JWT access token with optional additional claims."""
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINS))
    to_encode = {"sub": subject, "exp": expire}
    
    # Add additional claims if provided
    if additional_claims:
        to_encode.update(additional_claims)
    
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(
    subject: str, 
    additional_claims: Dict[str, Any] | None = None,
    expires_delta: timedelta | None = None
) -> str:
    """Create JWT refresh token with optional additional claims."""
    expire = datetime.utcnow() + (expires_delta or timedelta(days=REFRESH_TOKEN_EXPIRE))
    to_encode = {"sub": subject, "exp": expire, "type": "refresh"}
    
    # Add additional claims if provided
    if additional_claims:
        to_encode.update(additional_claims)
    
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)