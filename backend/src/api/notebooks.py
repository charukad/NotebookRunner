from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List, Dict
from src.infrastructure.database.session import get_db
from src.domain.models.notebook import Notebook, NotebookVersion
from src.schemas.notebook import NotebookResponse, NotebookVersionResponse
from src.services.notebook_service import upload_and_create_notebook

router = APIRouter(prefix="/notebooks", tags=["notebooks"])

@router.post("/upload", response_model=Dict[str, str], status_code=status.HTTP_201_CREATED)
def upload_notebook(project_id: UUID = Form(...), file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith(".ipynb"):
        raise HTTPException(status_code=400, detail="Must be a .ipynb file")
    try:
        notebook, version = upload_and_create_notebook(db, project_id, file)
        return {"notebook_id": str(notebook.id), "latest_version_id": str(version.id)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{notebook_id}", response_model=NotebookResponse)
def get_notebook(notebook_id: UUID, db: Session = Depends(get_db)):
    notebook = db.query(Notebook).filter(Notebook.id == notebook_id).first()
    if not notebook:
        raise HTTPException(status_code=404, detail="Notebook not found")
    return notebook

@router.get("/{notebook_id}/versions", response_model=List[NotebookVersionResponse])
def get_notebook_versions(notebook_id: UUID, db: Session = Depends(get_db)):
    versions = db.query(NotebookVersion).filter(NotebookVersion.notebook_id == notebook_id).order_by(NotebookVersion.version_number.desc()).all()
    return versions
