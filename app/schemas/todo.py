from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional


class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = "pending"
    priority: Optional[str] = "medium"
    due_date: Optional[datetime] = None


class TodoCreate(TodoBase):
    user_id: UUID


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[datetime] = None


class TodoResponse(TodoBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

class PaginatedTodoResponse(BaseModel):
    total: int
    page: int
    size: int
    items: list[TodoResponse]

    class Config:
        from_attributes = True