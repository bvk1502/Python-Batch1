from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.schemas.user import UserCreate
from fastapi import HTTPException

async def create_user(db: AsyncSession, user_in: UserCreate):
    user = User(**user_in.model_dump())
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def get_users(db: AsyncSession):
    result = await db.execute(select(User))
    return result.scalars().all()

#update_user
async def update_user(db: AsyncSession, user_id: int, user_in: UserCreate):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.update(user_in.model_dump())
    await db.commit()
    await db.refresh(user)
    return user
