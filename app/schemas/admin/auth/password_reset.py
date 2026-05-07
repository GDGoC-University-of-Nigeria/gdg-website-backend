from pydantic import BaseModel, field_validator
from app.core.validators.password import validate_strong_password


class AdminResetPasswordRequest(BaseModel):
    new_password: str

    @field_validator("new_password")
    @classmethod
    def password_strength(cls, value: str) -> str:
        return validate_strong_password(value)
