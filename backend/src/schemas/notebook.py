from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class NotebookVersionResponse(BaseModel):
    id: UUID
    notebook_id: UUID
    version_number: int
    file_url: str
    patched_file_url: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class NotebookResponse(BaseModel):
    id: UUID
    project_id: UUID
    name: str
    created_by: Optional[UUID] = None
    created_at: datetime

    class Config:
        from_attributes = True
