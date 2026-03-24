from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime
from uuid import UUID

class JobCreate(BaseModel):
    project_id: UUID
    notebook_version_id: UUID
    execution_backend: str = "colab"
    requested_gpu: bool = False
    parameters: Optional[Dict] = {}
    timeout_seconds: Optional[int] = 14400

class JobResponse(BaseModel):
    id: UUID
    project_id: UUID
    notebook_version_id: UUID
    status: str
    execution_backend: str
    requested_gpu: bool
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True

class JobStatusUpdate(BaseModel):
    status: str
