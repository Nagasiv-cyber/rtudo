from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserUpdate
from app.models.user import User

class UserService:
    def __init__(self, db: Session):
        
        self.repository = UserRepository(db)

    def create_user(self, user_in: UserCreate) -> User:
        """Executes business rules before delegating to the repository."""
        
        
        if not user_in.full_name.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Full name cannot be completely empty."
            )

        
        if "@" not in user_in.email or "." not in user_in.email.split("@")[-1]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid email format provided."
            )


        existing_user = self.repository.get_by_email(user_in.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this email already exists."
            )


        return self.repository.create(user_in)

    def get_user_by_id(self, user_id: str) -> User:
        """Retrieves a user, throwing a 404 if not found."""
        user = self.repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="User not found."
            )
        return user

    def update_user(self, user_id: str, update_data: UserUpdate) -> User:
        """Validates update logic before saving."""
        
        user = self.get_user_by_id(user_id)
        
        update_dict = update_data.model_dump(exclude_unset=True)
        
        return self.repository.update(user, update_dict)

    def delete_user(self, user_id: str) -> None:
        """Ensures the user exists before attempting deletion."""
        user = self.get_user_by_id(user_id)
        self.repository.delete(user)