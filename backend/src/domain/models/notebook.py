from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from .base import Base

class Notebook(Base):
    __tablename__ = "notebooks"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"))
    name = Column(String, nullable=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

class NotebookVersion(Base):
    __tablename__ = "notebook_versions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    notebook_id = Column(UUID(as_uuid=True), ForeignKey("notebooks.id"))
    version_number = Column(Integer, default=1)
    file_url = Column(String)  # MinIO path
    patched_file_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
