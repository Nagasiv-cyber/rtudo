from fastapi import FastAPI
from app.api.health import router as health_router
from app.config.settings import settings

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.project_name, 
        version=settings.version,
        debug=settings.debug
    )
    
    app.include_router(health_router, prefix="/api/v1")
    
    return app

# THIS IS THE LINE Uvicorn is looking for. 
# Make sure it is not indented!
app = create_app() 

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)