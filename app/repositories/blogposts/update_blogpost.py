"""Update a blogpost's content fields (author edit, pending state only)."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.blogpost import BlogPost
from app.schemas.blogpost import BlogPostUpdate


async def update_blogpost(
    db: AsyncSession,
    post: BlogPost,
    payload: BlogPostUpdate,
) -> BlogPost:
    """Apply partial updates to a blog post and flush to the database."""
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(post, field, value)
    await db.commit()
    await db.refresh(post)
    return post
