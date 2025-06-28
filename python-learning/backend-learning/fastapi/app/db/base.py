# app/db/base.py
# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.session import Base  # noqa
from app.models.base import BaseModel  # noqa
from app.models.user import User, UserRole  # noqa

# This is important for Alembic to detect all models
__all__ = ["Base", "BaseModel", "User", "UserRole"]
from app.models.user import User  # noqa