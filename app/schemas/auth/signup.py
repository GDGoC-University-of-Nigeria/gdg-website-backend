from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator
from uuid import UUID
import re

from app.core.validators.password import validate_strong_password


PHONE_REGEX = re.compile(r"^\+234[7-9][0-1]\d{8}$")


def normalize_ng_phone(phone: str) -> str:
    phone = phone.strip().replace(" ", "")

    # Convert local format to international
    if phone.startswith("0"):
        phone = "+234" + phone[1:]

    return phone


class SignUpRequest(BaseModel):
    email: EmailStr
    password: str
    confirm_password: str | None = None
    full_name: str
    phone: str | None = None

    @field_validator("password")
    @classmethod
    def password_strength(cls, value: str) -> str:
        return validate_strong_password(value)

    @field_validator("phone")
    @classmethod
    def validate_and_normalize_phone(cls, value: str | None) -> str | None:
        if value is None or value.strip() == "":
            return None
        phone = normalize_ng_phone(value)
        if not PHONE_REGEX.match(phone):
            raise ValueError(
                "Invalid Nigerian phone number. Use format +234XXXXXXXXXX"
            )
        return phone

    @model_validator(mode="after")
    def passwords_match(self):
        if self.confirm_password is not None and self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self


class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    full_name: str | None
    phone: str | None


# to be used for google auth
class GoogleAuthRequest(BaseModel):
    id_token: str
