"""
User schemas for the GDGoC UNN API.

This module defines Pydantic schemas for user-related operations including
profile completion, user creation, and user data retrieval.
"""

from pydantic import BaseModel, EmailStr
from typing import List, Literal


class CompleteProfileRequest(BaseModel):
    """
    Schema for completing a user's profile after initial registration.
    
    After OAuth registration, users can fill in additional profile information
    to help other community members learn about their skills and interests.
    
    Attributes:
        full_name (str): User's full name
        role (str): Role in the community (e.g., "Frontend Developer", "Designer")
        github (str, optional): GitHub profile URL or username
        avatar_url (str, optional): Profile picture URL
        skills (list[str]): List of technical skills
    """
    full_name: str
    role: str
    github: str | None = None
    avatar_url: str | None = None
    skills: List[str] = []


class UserCreate(BaseModel):
    """
    Schema for creating a new user during OAuth registration.
    
    This schema is used when a user first authenticates via Google OAuth.
    Most fields are optional as they can be filled in later during profile completion.
    
    Attributes:
        email (EmailStr): User's email address from OAuth provider
        provider (Literal["google"]): OAuth provider (currently only Google)
        provider_user_id (str): User ID from the OAuth provider
        full_name (str, optional): User's full name from OAuth
        role (str, optional): Community role
        github (str, optional): GitHub profile
        avatar_url (str, optional): Profile picture from OAuth
        skills (list[str]): Technical skills (empty by default)
        profile_complete (bool): Profile completion status (False by default)
    """
    email: EmailStr
    provider: Literal["google"]
    provider_user_id: str
    full_name: str | None = None
    role: str | None = None
    github: str | None = None
    avatar_url: str | None = None
    skills: list[str] = []
    profile_complete: bool = False


class UserRead(BaseModel):
    """
    Schema for reading user data from the API.
    
    This schema is used when returning user information in API responses.
    It excludes sensitive fields like provider_user_id.
    
    Attributes:
        id (str): User's unique identifier
        email (EmailStr): User's email address
        full_name (str, optional): User's full name
        role (str, optional): Community role
        github (str, optional): GitHub profile
        avatar_url (str, optional): Profile picture URL
        skills (list[str]): List of technical skills
    """
    id: str
    email: EmailStr
    full_name: str | None
    role: str | None
    github: str | None
    avatar_url: str | None
    skills: List[str]