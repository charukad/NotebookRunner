from fastapi import UploadFile
from sqlalchemy.orm import Session
from uuid import UUID, uuid4
import json
from src.domain.models.notebook import Notebook, NotebookVersion
from src.infrastructure.storage.minio_client import get_minio_client

BUCKET_NAME = "notebooks-original"

def ensure_bucket_exists(client):
    found = client.bucket_exists(BUCKET_NAME)
    if not found:
        client.make_bucket(BUCKET_NAME)

def upload_and_create_notebook(db: Session, project_id: UUID, file: UploadFile, user_id: UUID = None):
    content = file.file.read()
    try:
        notebook_data = json.loads(content)
        if "cells" not in notebook_data:
            raise ValueError("Invalid notebook structure")
    except Exception as e:
        raise ValueError("File is not a valid Jupyter Notebook JSON")

    minio_client = get_minio_client()
    ensure_bucket_exists(minio_client)
    
    file_id = uuid4()
    object_name = f"{project_id}/{file_id}.ipynb"
    
    file.file.seek(0)
    minio_client.put_object(
        BUCKET_NAME,
        object_name,
        file.file,
        len(content),
        content_type="application/x-ipynb+json"
    )
    file_url = f"s3://{BUCKET_NAME}/{object_name}"

    notebook = Notebook(project_id=project_id, name=file.filename, created_by=user_id)
    db.add(notebook)
    db.commit()
    db.refresh(notebook)

    version = NotebookVersion(notebook_id=notebook.id, version_number=1, file_url=file_url)
    db.add(version)
    db.commit()
    db.refresh(version)

    return notebook, version
