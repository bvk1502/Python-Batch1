from app.models.base import BaseModel
from app.models.user import User, UserRole

# This is important for Alembic to detect models
__all__ = ["User"]