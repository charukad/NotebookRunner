from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List
from src.infrastructure.database.session import get_db
from src.domain.models.workspace import Workspace
from src.schemas.workspace import WorkspaceCreate, WorkspaceResponse, WorkspaceUpdate

router = APIRouter(prefix="/workspaces", tags=["workspaces"])

@router.post("/", response_model=WorkspaceResponse, status_code=status.HTTP_201_CREATED)
def create_workspace(workspace: WorkspaceCreate, db: Session = Depends(get_db)):
    db_workspace = Workspace(**workspace.model_dump())
    db.add(db_workspace)
    db.commit()
    db.refresh(db_workspace)
    return db_workspace

@router.get("/", response_model=List[WorkspaceResponse])
def get_workspaces(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return db.query(Workspace).offset(skip).limit(limit).all()

@router.get("/{workspace_id}", response_model=WorkspaceResponse)
def get_workspace(workspace_id: UUID, db: Session = Depends(get_db)):
    db_workspace = db.query(Workspace).filter(Workspace.id == workspace_id).first()
    if not db_workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    return db_workspace
