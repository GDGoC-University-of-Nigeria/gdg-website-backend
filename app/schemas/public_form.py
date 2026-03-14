from datetime import datetime
from enum import Enum
from typing import Any, Dict

from pydantic import BaseModel, EmailStr, Field


class PublicFormKind(str, Enum):
    APPLY_TO_SPEAK = "apply_to_speak"
    VOLUNTEER = "volunteer"
    CONTACT = "contact"


class BasePublicForm(BaseModel):
    name: str = Field(..., min_length=2, max_length=200)
    email: EmailStr
    phone: str | None = Field(default=None, max_length=50)
    message: str | None = Field(default=None, max_length=4000)


class ApplyToSpeakForm(BasePublicForm):
    topic: str = Field(..., min_length=3, max_length=300)
    abstract: str = Field(..., min_length=10, max_length=4000)
    preferredTime: str | None = Field(default=None, max_length=200)


class VolunteerForm(BasePublicForm):
    interests: str = Field(..., min_length=3, max_length=2000)
    availability: str = Field(..., min_length=3, max_length=2000)


class ContactForm(BasePublicForm):
    subject: str = Field(..., min_length=3, max_length=200)


FORM_KIND_TO_MODEL: Dict[PublicFormKind, type[BasePublicForm]] = {
    PublicFormKind.APPLY_TO_SPEAK: ApplyToSpeakForm,
    PublicFormKind.VOLUNTEER: VolunteerForm,
    PublicFormKind.CONTACT: ContactForm,
}


class PublicFormSubmitRequest(BaseModel):
    kind: PublicFormKind
    payload: Dict[str, Any]


class PublicFormSubmitResponse(BaseModel):
    message: str
    submitted_at: datetime

