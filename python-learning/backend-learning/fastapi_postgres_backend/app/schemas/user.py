from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    email: str
    name: str
    

class UserCreate(UserBase):
    pass

class UserOut(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    is_deleted: bool

    class Config:
        orm_mode = True
