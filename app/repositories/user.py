from sqlalchemy.orm import Session
from app.models.user import User    
from app.schemas.user import UserCreate

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user_create: UserCreate) -> User:
        """Create a new user in the database."""

        fake_hashed_password = user_create.password + "notreallyhashed"
        
        db_user = User(
            full_name=user_create.full_name,
            email=user_create.email,
            password_hash=fake_hashed_password
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_by_id(self, user_id: str) -> User | None:
        """Retrieves a user by their UUID."""
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> User | None:
        """Retrieves a user by their email address (used for login/duplicate checks)."""
        return self.db.query(User).filter(User.email == email).first()

    def update(self, db_user: User, update_data: dict) -> User:
        """Updates an existing user's attributes."""
        for field, value in update_data.items():
            setattr(db_user, field, value)
            
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def delete(self, db_user: User) -> None:
        """Removes a user from the database."""
        self.db.delete(db_user)
        self.db.commit()