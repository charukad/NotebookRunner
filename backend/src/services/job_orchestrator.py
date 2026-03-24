from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime
from src.domain.models.job import Job
from src.schemas.job import JobCreate
import asyncio
# Need to import or initialize a publisher locally if calling from sync contexts
from src.infrastructure.queue.rabbitmq_client import publisher


ALLOWED_TRANSITIONS = {
    "created": ["queued", "failed", "cancelled"],
    "queued": ["preparing", "cancelled"],
    "preparing": ["patched", "failed"],
    "patched": ["launching", "failed"],
    "launching": ["running", "failed"],
    "running": ["collecting_artifacts", "failed", "timed_out", "cancelled"],
    "collecting_artifacts": ["completed", "failed"],
    "completed": [],
    "failed": [],
    "timed_out": [],
    "cancelled": []
}

def create_job(db: Session, job_data: JobCreate, user_id: UUID):
    db_job = Job(
        project_id=job_data.project_id,
        notebook_version_id=job_data.notebook_version_id,
        user_id=user_id,
        execution_backend=job_data.execution_backend,
        requested_gpu=job_data.requested_gpu,
        status="created"
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    
    update_job_status(db, db_job.id, "queued")
    
    # Publish to RabbitMQ using asyncio.run for the MVP sync FastAPI route
    payload = {
        "job_id": str(db_job.id),
        "project_id": str(db_job.project_id),
        "execution_backend": db_job.execution_backend,
        "requested_gpu": db_job.requested_gpu,
        "patched_notebook_path": "s3://notebooks-original/placeholder.ipynb" # in real life from notebook metadata
    }
    
    # Ideally the API routes are async, but for sync, we block until published
    loop = asyncio.get_event_loop()
    if loop.is_running():
        asyncio.create_task(publisher.publish("job.execute", payload))
    else:
        asyncio.run(publisher.publish("job.execute", payload))
    
    return db_job

def update_job_status(db: Session, job_id: UUID, new_status: str):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise ValueError("Job not found")
        
    current_status = job.status
    if new_status not in ALLOWED_TRANSITIONS.get(current_status, []):
        raise ValueError(f"Invalid transition from {current_status} to {new_status}")
        
    job.status = new_status
    if new_status == "running":
        job.started_at = datetime.utcnow()
    elif new_status in ["completed", "failed", "cancelled", "timed_out"]:
        job.completed_at = datetime.utcnow()
        
    db.commit()
    db.refresh(job)
    return job
