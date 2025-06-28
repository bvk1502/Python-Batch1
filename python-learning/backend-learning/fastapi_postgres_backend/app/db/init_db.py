from app.crud.user import create_user
from app.core.config import settings
from app.schemas.user import UserCreate

async def init_db(session):
    user = UserCreate(email=settings.FIRST_SUPERUSER_EMAIL, name="Admin")
    await create_user(session, user)
