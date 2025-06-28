from sqlalchemy import Column, Integer, String, Boolean
from app.db.base_class import Base
from datetime import datetime
from sqlalchemy.types import DateTime

class DBBaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)
    is_deleted = Column(Boolean, default=False)
