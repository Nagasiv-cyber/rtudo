from sqlalchemy.orm import Session
from app.models.todo import Todo
from app.schemas.todo import TodoCreate

class TodoRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, todo_in: TodoCreate) -> Todo:
        """Creates a new todo item."""
        
        db_todo = Todo(**todo_in.model_dump())
        self.db.add(db_todo)
        self.db.commit()
        self.db.refresh(db_todo)
        return db_todo

    def get_all(
        self, 
        skip: int = 0, 
        limit: int = 10, 
        search: str | None = None, 
        status: str | None = None, 
        priority: str | None = None
    ) -> tuple[int, list[Todo]]:
        """Retrieves todos with dynamic filtering and pagination."""
       
        query = self.db.query(Todo)

        if search:
            query = query.filter(Todo.title.ilike(f"%{search}%"))
        if status:
            query = query.filter(Todo.status == status)
        if priority:
            query = query.filter(Todo.priority == priority)

        total = query.count()

        items = query.order_by(Todo.created_at.desc()).offset(skip).limit(limit).all()

        return total, items

    def get_by_id(self, todo_id: str) -> Todo | None:
        """Retrieves a specific todo by ID."""
        return self.db.query(Todo).filter(Todo.id == todo_id).first()

    def update(self, db_todo: Todo, update_data: dict) -> Todo:
        """Updates an existing todo."""
        for field, value in update_data.items():
            setattr(db_todo, field, value)
        self.db.commit()
        self.db.refresh(db_todo)
        return db_todo

    def delete(self, db_todo: Todo) -> None:
        """Deletes a todo."""
        self.db.delete(db_todo)
        self.db.commit()