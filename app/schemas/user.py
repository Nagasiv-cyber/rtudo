from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional
class UserCreate(BaseModel):
    full_name: str
    email: str
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

class UserResponse(BaseModel):
    id: UUID
    full_name: str
    email: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True