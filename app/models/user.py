"""
User model for the GDGoC UNN API.

This module defines the User model representing community members who register
on the GDGoC UNN platform. Users authenticate via Google OAuth and can complete
their profiles with additional information.
"""

from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base


class User(Base):
    """
    User model representing a GDGoC UNN community member.
    
    Users register through Google OAuth authentication and can optionally complete
    their profiles with additional information like skills, GitHub profile, and role.
    
    Attributes:
        id (UUID): Unique identifier for the user
        email (str): User's email address (unique, from Google OAuth)
        provider (str): OAuth provider name (currently only "google")
        provider_user_id (str): User ID from the OAuth provider
        full_name (str, optional): User's full name
        role (str, optional): User's role in the community (e.g., "Frontend Developer", "Designer")
        github (str, optional): GitHub profile URL or username
        avatar_url (str, optional): URL to user's profile picture
        skills (list[str]): List of user's technical skills
        profile_complete (bool): Whether the user has completed their profile
        is_active (bool): Whether the user account is active
        created_at (datetime): Timestamp when the user registered
    
    Relationships:
        events: Events created by this user (to be implemented)
        projects: Projects created by this user (to be implemented)
        blogposts: Blog posts authored by this user (to be implemented)
        applications: Project applications submitted by this user (to be implemented)
    """

    __tablename__ = "users"

    # Authentication fields
    id = Column(UUID, primary_key=True)  # Unique user identifier
    email = Column(String, unique=True, nullable=False)  # Email from Google OAuth
    provider = Column(String, nullable=False)  # OAuth provider (e.g., "google")
    provider_user_id = Column(String, nullable=False)  # Google user ID (google sub)
    
    # Profile fields (optional, completed after registration)
    full_name = Column(String, nullable=True)  # User's display name
    role = Column(String, nullable=True)  # Community role/position
    github = Column(String, nullable=True)  # GitHub profile for collaboration
    avatar_url = Column(String, nullable=True)  # Profile picture URL
    skills = Column(ARRAY(String), default=[])  # Technical skills array
    
    # Account status fields
    profile_complete = Column(Boolean, default=False)  # Tracks profile completion
    is_active = Column(Boolean, default=True)  # Account activation status
    created_at = Column(DateTime, default=func.now())  # Registration timestamp

    # Relationships (commented out until implemented)
    # events = relationship("Event", back_populates="creator")
    # projects = relationship("Project", back_populates="creator")
    # blogposts = relationship("BlogPost", back_populates="author")
    # applications = relationship("Applicant", back_populates="user")