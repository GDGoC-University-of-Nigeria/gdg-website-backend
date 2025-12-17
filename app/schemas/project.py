"""
Project schemas for the GDGoC UNN API.

This module defines Pydantic schemas for project-related operations including
creating and reading project data.
"""

from pydantic import BaseModel, ConfigDict
from datetime import date
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


class ProjectCreate(BaseModel):
    """
    Schema for creating a new project.
    
    This schema defines the fields required when creating a new collaborative
    project in the GDGoC UNN community.
    
    Attributes:
        title (str): Project name
        description (str): Detailed project description and goals
        duration (str, optional): Expected project duration (e.g., "3 months")
        start_date (date, optional): Project start date
        end_date (date, optional): Project completion/deadline date
        github_repo (str, optional): GitHub repository URL
        demo_video_url (str, optional): URL to project demo or presentation
    """
    title: str
    description: str
    duration: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    github_repo: str | None = None
    demo_video_url: str | None = None


class ProjectRead(ProjectCreate):
    """
    Schema for reading project data from the API.
    
    Extends ProjectCreate with database-generated fields like id, status,
    and created_at timestamp.
    
    Attributes:
        id (UUID): Unique project identifier
        status (ProjectStatus): Current project status (ongoing/completed)
        created_at (str): Timestamp when the project was created
    """
    id: UUID
    status: ProjectStatus
    created_at: str

    model_config = ConfigDict(from_attributes=True)
