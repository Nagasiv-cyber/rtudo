from fastapi import APIRouter, Depends, status, Query
from typing import Optional
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.todo import TodoCreate, TodoResponse, TodoUpdate, PaginatedTodoResponse
from app.services.todo import TodoService

router = APIRouter(prefix="/todos", tags=["Todos"])

@router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(todo_in: TodoCreate, db: Session = Depends(get_db)):
    return TodoService(db).create_todo(todo_in)
# NEW CODE - PASTE THIS INSTEAD
@router.get("/", response_model=PaginatedTodoResponse)
def get_todos(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Search by title"),
    status: Optional[str] = Query(None, description="Filter by status"),
    priority: Optional[str] = Query(None, description="Filter by priority"),
    db: Session = Depends(get_db)
):
    return TodoService(db).get_todos(
        page=page, 
        size=size, 
        search=search, 
        status=status, 
        priority=priority
    )

@router.get("/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: str, db: Session = Depends(get_db)):
    return TodoService(db).get_todo(todo_id)

@router.put("/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: str, todo_in: TodoUpdate, db: Session = Depends(get_db)):
    return TodoService(db).update_todo(todo_id, todo_in)

@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: str, db: Session = Depends(get_db)):
    TodoService(db).delete_todo(todo_id)