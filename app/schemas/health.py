from pydantic import BaseModel

class HealthResponse(BaseModel):
    status: str
    database: str
    project_name: str
    version: str