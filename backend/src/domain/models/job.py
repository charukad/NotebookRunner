from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Integer, JSON
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from .base import Base

class Job(Base):
    __tablename__ = "jobs"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"))
    notebook_version_id = Column(UUID(as_uuid=True), ForeignKey("notebook_versions.id"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    status = Column(String, default="created")
    execution_backend = Column(String, default="colab")
    requested_gpu = Column(Boolean, default=False)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
