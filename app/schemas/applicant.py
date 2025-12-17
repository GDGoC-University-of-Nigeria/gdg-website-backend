"""
Applicant schemas for the GDGoC UNN API.

This module defines Pydantic schemas for managing project collaboration
applications and contributor approvals.
"""

from pydantic import BaseModel, ConfigDict
from uuid import UUID


class ApplicantCreate(BaseModel):
    """
    Schema for creating a project application.
    
    When a user wants to contribute to a project, they submit an application
    specifying their desired role. The user_id is automatically set from
    the authenticated user.
    
    Attributes:
        project_id (UUID): ID of the project to apply to
        role (str): Desired role in the project (e.g., "Frontend Developer", "Designer")
    
    Notes:
        - Applications are created with is_contributor=False
        - Project owners can review and approve applications
        - Once approved, is_contributor is set to True
    """
    project_id: UUID
    role: str


class ApplicantRead(BaseModel):
    """
    Schema for reading applicant data from the API.
    
    Used when retrieving application information, including approval status.
    
    Attributes:
        id (UUID): Unique application identifier
        user_id (UUID): ID of the user who applied
        project_id (UUID): ID of the project applied to
        role (str): Desired role in the project
        is_contributor (bool): Whether the application has been approved
    
    Notes:
        - is_contributor=False means pending approval
        - is_contributor=True means approved and can contribute
    """
    id: UUID
    user_id: UUID
    project_id: UUID
    role: str
    is_contributor: bool

    model_config = ConfigDict(from_attributes=True)
