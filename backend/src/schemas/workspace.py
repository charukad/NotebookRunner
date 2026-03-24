from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class WorkspaceBase(BaseModel):
    name: str

class WorkspaceCreate(WorkspaceBase):
    pass

class WorkspaceUpdate(BaseModel):
    name: Optional[str] = None
    plan: Optional[str] = None

class WorkspaceResponse(WorkspaceBase):
    id: UUID
    owner_id: Optional[UUID] = None
    plan: str
    created_at: datetime

    class Config:
        from_attributes = True
