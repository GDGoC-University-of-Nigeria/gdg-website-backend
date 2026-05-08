"""Delete a blogpost from the database."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.blogpost import BlogPost


async def delete_blogpost(db: AsyncSession, post: BlogPost) -> None:
    """Permanently delete a blog post and cascade its likes/comments."""
    await db.delete(post)
    await db.commit()
