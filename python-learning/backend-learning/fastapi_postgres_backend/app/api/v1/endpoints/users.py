from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate, UserOut
from app.crud.user import create_user, get_users, update_user
from app.db.session import get_db

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserOut)
async def api_create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await create_user(db, user)

@router.get("/", response_model=list[UserOut])
async def api_get_users(db: AsyncSession = Depends(get_db)):
    return await get_users(db)

#update user
@router.put("/{user_id}", response_model=UserOut)
async def api_update_user(user_id: int, user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await update_user(db, user_id, user)
