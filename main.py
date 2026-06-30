from fastapi import FastAPI
from app.config.settings import settings
from app.api.health import router as health_router

from app.api.todo import router as todos_router 

def create_app() -> FastAPI:
    
    app = FastAPI(
        title=settings.project_name,
        version=settings.version,
    )
    
    app.include_router(health_router, prefix="/api/v1")
    app.include_router(todos_router, prefix="/api/v1")
    
    return app

app = create_app()