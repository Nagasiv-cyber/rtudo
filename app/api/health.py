from fastapi import APIRouter, status
from app.schemas.health import HealthResponse
from app.config.settings import settings

router = APIRouter()

@router.get(
    "/health", 
    response_model=HealthResponse, 
    status_code=status.HTTP_200_OK,
    tags=["System"]
)
async def health_check() -> HealthResponse:
    return HealthResponse(
        status="healthy",
        project_name=settings.project_name,
        version=settings.version
    )