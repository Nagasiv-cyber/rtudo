from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.schemas.health import HealthResponse
from app.config.settings import settings
from app.db.session import get_db

router = APIRouter()

@router.get(
    "/health", 
    response_model=HealthResponse, 
    status_code=status.HTTP_200_OK,
    tags=["System"]
)
async def health_check(db: Session = Depends(get_db)) -> HealthResponse:
    """
    Check the health status of the API and the Database connection.
    """
    try:
        # Execute a lightweight query to verify DB connectivity
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        # If the DB is unavailable or credentials are bad, this catches it
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database connection failed: {str(e)}"
        )

    return HealthResponse(
        status="healthy",
        database=db_status,
        project_name=settings.project_name,
        version=settings.version
    )