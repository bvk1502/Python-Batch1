from sqlalchemy.orm import Session
from app.core.config import settings
from app.services.user import create_user
from app.schemas.user import UserCreate
from app.models.user import UserRole, User

def init_db(db: Session) -> None:
    # Create first superuser
    user = db.query(User).filter(User.email == settings.FIRST_SUPERUSER_EMAIL).first()
    if not user:
        """pass"""
        # user_in = UserCreate(
        #     email=settings.FIRST_SUPERUSER_EMAIL,
        #     password=settings.FIRST_SUPERUSER_PASSWORD,
        #     full_name="Initial Super User",
        #     role=UserRole.ADMIN,
        #     is_active=True,
        # )
        # create_user(db, user_in) 