from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from .base import Base

class JobMetric(Base):
    __tablename__ = "job_metrics"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_id = Column(UUID(as_uuid=True), ForeignKey("jobs.id"))
    metric_name = Column(String, nullable=False)
    metric_value = Column(Float, nullable=False)
    step = Column(Integer, nullable=True)
    recorded_at = Column(DateTime, default=datetime.utcnow)
