from app.repository.user import UserRepository
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from sqlalchemy.orm import Session

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        
    def get_users(self, db: Session, skip: int = 0, limit: int = 100) -> list[User]:
        return self.user_repository.get_users(db, skip=skip, limit=limit)

    def get_user_by_email(self, db: Session, email: str) -> User:
        return self.user_repository.get_user_by_email(db, email)
    
    def get_user_by_id(self, db: Session, user_id: int) -> User:
        return self.user_repository.get_user_by_id(db, user_id)
    
    def create_user(self, db: Session, user_in: UserCreate) -> User:
        return self.user_repository.create_user(db, user_in)
    
    def update_user(self, db: Session, db_user: User, user_in: UserUpdate) -> User:
        return self.user_repository.update_user(db, db_user, user_in)