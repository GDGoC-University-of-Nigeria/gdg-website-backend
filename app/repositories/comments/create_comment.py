from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.models.comment import Comment
from app.schemas.comment import CommentCreate


async def create_comment(
    db: AsyncSession,
    blogpost_id: UUID,
    user_id: UUID,
    payload: CommentCreate,
) -> Comment:
    comment = Comment(
        content=payload.content,
        user_id=user_id,
        blogpost_id=blogpost_id,
    )
    db.add(comment)
    await db.commit()
    await db.refresh(comment)
    return comment
