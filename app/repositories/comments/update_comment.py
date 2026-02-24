from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.comment import Comment
from app.schemas.comment import CommentUpdate


async def update_comment(
    db: AsyncSession,
    comment: Comment,
    payload: CommentUpdate,
) -> Comment:
    comment.content = payload.content
    comment.updated_at = datetime.utcnow()
    db.add(comment)
    await db.commit()
    await db.refresh(comment)
    return comment
