"""
Project schemas for the GDGoC UNN API.

This module defines Pydantic schemas for project-related operations including
creating and reading project data, managing contributors, and project types.
"""

from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from uuid import UUID
from enum import Enum


class ProjectStatus(str, Enum):
    """
    Enumeration of possible project statuses.
    """
    ongoing = "ongoing"
    completed = "completed"


class ProjectApprovalStatus(str, Enum):
    """
    Admin-controlled approval state.
    """
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class ProjectType(str, Enum):
  
    personal = "personal"
    community = "community"


from app.schemas.user import UserBasic



class ProjectCreate(BaseModel):
   
    project_type: ProjectType
    title: str
    description: str
    duration: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    github_repo: str | None = None
    demo_video_url: str | None = None


class ProjectUpdate(BaseModel):
  
    title: str | None = None
    description: str | None = None
    duration: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    github_repo: str | None = None
    demo_video_url: str | None = None
    status: ProjectStatus | None = None


class ProjectApproveReject(BaseModel):
    """Admin approve/reject payload — reason is optional."""
    reason: str | None = None


class ProjectFeatureToggle(BaseModel):
    """Admin feature/un-feature payload."""
    is_featured: bool


class ProjectRead(BaseModel):
 
    id: UUID
    project_type: ProjectType
    creator_id: UUID
    title: str
    description: str
    duration: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    github_repo: str | None = None
    demo_video_url: str | None = None
    status: ProjectStatus
    approval_status: ProjectApprovalStatus
    is_featured: bool
    rejection_reason: str | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProjectContributorCreate(BaseModel):
 
    user_id: UUID
    role: str


class ProjectContributorRead(BaseModel):
   
    id: UUID
    user_id: UUID
    role: str
    added_at: datetime
    user: UserBasic

    model_config = ConfigDict(from_attributes=True)


class ProjectDetailRead(ProjectRead):
 
    creator: UserBasic
    contributors: list[ProjectContributorRead] = []

    model_config = ConfigDict(from_attributes=True)
