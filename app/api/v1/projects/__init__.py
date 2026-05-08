"""
Projects API module.

This module imports and registers all project-related endpoints.
"""

from .router import router
from . import (
    create_project,
    get_all_projects,
    my_applications,
    get_project_by_id,
    update_project,
    delete_project,
    add_contributor,
    remove_contributor,
    get_contributors,
    apply,
    withdraw_application,
    get_applications,
    approve_application,
    reject_application,
)

__all__ = ["router"]
