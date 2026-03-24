from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List
from src.infrastructure.database.session import get_db
from src.domain.models.job import Job
from src.schemas.job import JobCreate, JobResponse, JobStatusUpdate
from src.services.job_orchestrator import create_job, update_job_status

router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.post("/", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
def route_create_job(job_in: JobCreate, db: Session = Depends(get_db)):
    # Assuming user_id is injected via auth middleware in real app; simulating for MVP
    user_id = None 
    job = create_job(db, job_in, user_id)
    return job

@router.get("/{job_id}", response_model=JobResponse)
def get_job(job_id: UUID, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.patch("/{job_id}/status", response_model=JobResponse)
def patch_job_status(job_id: UUID, status_update: JobStatusUpdate, db: Session = Depends(get_db)):
    try:
        job = update_job_status(db, job_id, status_update.status)
        return job
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
