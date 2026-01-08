from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator
from uuid import UUID
import re


PHONE_REGEX = re.compile(r"^\+234[7-9][0-1]\d{8}$")


def normalize_ng_phone(phone: str) -> str:
    phone = phone.strip().replace(" ", "")

    # Convert local format to international
    if phone.startswith("0"):
        phone = "+234" + phone[1:]

    return phone


class SignUpRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    confirm_password: str
    full_name: str
    phone: str

    @field_validator("phone")
    @classmethod
    def validate_and_normalize_phone(cls, value: str) -> str:
        phone = normalize_ng_phone(value)

        if not PHONE_REGEX.match(phone):
            raise ValueError(
                "Invalid Nigerian phone number. Use format +234XXXXXXXXXX"
            )

        return phone
    
    @model_validator(mode="after")
    def passwords_match(self):
        if self.password != self.confirm_password:
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
