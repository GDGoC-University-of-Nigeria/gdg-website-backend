"""
Community blogposts API module.

Route order matters: /me must be registered before /{post_id} to avoid
the path parameter swallowing the literal 'me' segment.
Similarly, /{post_id}/like and /{post_id}/comments are registered after
the exact /me route but before the bare /{post_id} catch-all.
"""

from .router import router
from . import (
    submit_blogpost,
    list_blogposts,
    get_my_blogposts,   # /me — must come before /{post_id}
    like_blogpost,      # /{post_id}/like
    post_comment,       # /{post_id}/comments POST
    get_comments,       # /{post_id}/comments GET
    niches,             # /niches (static before /{post_id})
    get_blogpost,       # /{post_id} — catch-all last
    update_blogpost,
    delete_blogpost,
)

__all__ = ["router"]

