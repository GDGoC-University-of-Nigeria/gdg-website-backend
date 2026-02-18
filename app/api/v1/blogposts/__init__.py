"""
Community blogposts API module.

Route order matters: /me must be registered before /{post_id} to avoid
the path parameter swallowing the literal 'me' segment.
"""

from .router import router
from . import (
    submit_blogpost,
    list_blogposts,
    get_my_blogposts,  # must come before get_blogpost
    get_blogpost,
)

__all__ = ["router"]
