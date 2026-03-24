from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from .base import Base

class MLModel(Base):
    __tablename__ = "models"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"))
    name = Column(String, nullable=False)
    framework = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class MLModelVersion(Base):
    __tablename__ = "model_versions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    model_id = Column(UUID(as_uuid=True), ForeignKey("models.id"))
    job_id = Column(UUID(as_uuid=True), ForeignKey("jobs.id"))
    version = Column(String, nullable=False)
    artifact_id = Column(UUID(as_uuid=True)) # no strict foreign key to artifacts for flexibility
    accuracy = Column(Float, nullable=True)
    is_best = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
