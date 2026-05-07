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
    
    Attributes:
        ongoing: Project is currently active and accepting contributions
        completed: Project has been finished
    """
    ongoing = "ongoing"
    completed = "completed"


class ProjectType(str, Enum):
    """
    Enumeration of project types.
    
    Attributes:
        personal: Project created by a regular community member
        community: Official community project created by an admin
    """
    personal = "personal"
    community = "community"


from app.schemas.user import UserBasic



class ProjectCreate(BaseModel):
    """
    Schema for creating a new project.
    
    This schema defines the fields required when creating a new collaborative
    project in the GDGoC UNN community.
    
    Attributes:
        project_type (ProjectType): Type of project (personal or community)
        title (str): Project name
        description (str): Detailed project description and goals
        duration (str, optional): Expected project duration (e.g., "3 months")
        start_date (date, optional): Project start date
        end_date (date, optional): Project completion/deadline date
        github_repo (str, optional): GitHub repository URL
        demo_video_url (str, optional): URL to project demo or presentation
    """
    project_type: ProjectType
    title: str
    description: str
    duration: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    github_repo: str | None = None
    demo_video_url: str | None = None


class ProjectUpdate(BaseModel):
    """
    Schema for updating an existing project.
    
    All fields are optional to allow partial updates.
    Note: project_type and creator_id cannot be updated.
    """
    title: str | None = None
    description: str | None = None
    duration: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    github_repo: str | None = None
    demo_video_url: str | None = None
    status: ProjectStatus | None = None


class ProjectRead(BaseModel):
    """
    Schema for reading basic project data from the API.
    
    Attributes:
        id (UUID): Unique project identifier
        project_type (ProjectType): Type of project
        creator_id (UUID): ID of the project creator
        title (str): Project name
        description (str): Project description
        duration (str, optional): Project duration
        start_date (date, optional): Project start date
        end_date (date, optional): Project end date
        github_repo (str, optional): GitHub repository URL
        demo_video_url (str, optional): Demo video URL
        status (ProjectStatus): Current project status
        created_at (datetime): Creation timestamp
    """
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
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProjectContributorCreate(BaseModel):
    """
    Schema for adding a contributor to a project.
    
    Attributes:
        user_id (UUID): ID of the user to add as contributor
        role (str): Contributor's role in the project
    """
    user_id: UUID
    role: str


class ProjectContributorRead(BaseModel):
    """
    Schema for reading contributor data.
    
    Attributes:
        id (UUID): Contributor record identifier
        user_id (UUID): User ID of the contributor
        role (str): Contributor's role
        added_at (datetime): When they were added
        user (UserBasic): Nested user details
    """
    id: UUID
    user_id: UUID
    role: str
    added_at: datetime
    user: UserBasic

    model_config = ConfigDict(from_attributes=True)


class ProjectDetailRead(ProjectRead):
    """
    Detailed project schema with creator and contributors.
    
    Extends ProjectRead with relational data.
    
    Attributes:
        creator (UserBasic): Project creator details
        contributors (list[ProjectContributorRead]): List of contributors
    """
    creator: UserBasic
    contributors: list[ProjectContributorRead] = []

    model_config = ConfigDict(from_attributes=True)
