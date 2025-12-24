from typing import Any, Dict, Optional, Union
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.schemas.user import UserCreate, CompleteProfileRequest

async def get_by_email(db: AsyncSession, email: str) -> Optional[User]:
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()

async def get_by_google_id(db: AsyncSession, google_id: str) -> Optional[User]:
    result = await db.execute(select(User).filter(User.provider_user_id == google_id))
    return result.scalars().first()

async def create_from_google(db: AsyncSession, obj_in: UserCreate) -> User:
    db_obj = User(
        email=obj_in.email,
        provider=obj_in.provider,
        provider_user_id=obj_in.provider_user_id,
        full_name=obj_in.full_name,
        role=obj_in.role,
        github=obj_in.github,
        avatar_url=obj_in.avatar_url,
        skills=obj_in.skills,
        profile_complete=obj_in.profile_complete
    )
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

async def update(
    db: AsyncSession, *, db_obj: User, obj_in: Union[CompleteProfileRequest, Dict[str, Any]]
) -> User:
    if isinstance(obj_in, dict):
        update_data = obj_in
    else:
        update_data = obj_in.model_dump(exclude_unset=True)
        
    for field in update_data:
        if hasattr(db_obj, field):
            setattr(db_obj, field, update_data[field])
            
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj
