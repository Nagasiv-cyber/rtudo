from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories.todo import TodoRepository
from app.schemas.todo import TodoCreate, TodoUpdate
from app.models.todo import Todo

class TodoService:
    def __init__(self, db: Session):
        self.repository = TodoRepository(db)

    def create_todo(self, todo_in: TodoCreate) -> Todo:
        if not todo_in.title.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Title cannot be empty."
            )
        return self.repository.create(todo_in)

    def get_todos(
        self, 
        page: int = 1, 
        size: int = 10, 
        search: str | None = None, 
        status: str | None = None, 
        priority: str | None = None
    ) -> dict:
        """Calculates pagination offsets and formats the paginated response."""
        skip = (page - 1) * size
        
        total, items = self.repository.get_all(
            skip=skip, 
            limit=size, 
            search=search, 
            status=status, 
            priority=priority
        )
        
        return {
            "total": total,
            "page": page,
            "size": size,
            "items": items
        }
    
    def get_todo(self, todo_id: str) -> Todo:
        todo = self.repository.get_by_id(todo_id)
        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Todo not found."
            )
        return todo


    def update_todo(self, todo_id: str, update_data: TodoUpdate) -> Todo:
        todo = self.get_todo(todo_id)
        update_dict = update_data.model_dump(exclude_unset=True)
        return self.repository.update(todo, update_dict)

    def delete_todo(self, todo_id: str) -> None:
        todo = self.get_todo(todo_id)
        self.repository.delete(todo)