from sqlalchemy.ext.asyncio import AsyncSession

from app.models.comment import Comment


async def delete_comment(
    db: AsyncSession,
    comment: Comment,
) -> None:
    await db.delete(comment)
    await db.commit()
