"""
Authentication schemas for the GDGoC UNN API.

This module defines Pydantic schemas for Google OAuth authentication.
"""

from pydantic import BaseModel


class GoogleAuthRequest(BaseModel):
    """
    Schema for Google OAuth authentication request.
    
    This schema is used when a user authenticates via Google OAuth.
    The frontend sends the ID token received from Google, which is then
    verified on the backend.
    
    Attributes:
        id_token (str): JWT token from Google OAuth containing user information
    
    Usage:
        The frontend obtains this token from Google's OAuth flow and sends it
        to the backend for verification. The backend validates the token and
        creates or retrieves the user account.
    
    Notes:
        - Token verification ensures the user is authenticated by Google
        - User information is extracted from the verified token
        - New users are automatically created on first login
    """
    id_token: str
