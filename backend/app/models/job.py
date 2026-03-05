from sqlalchemy import Column, Integer, String, Float, Date, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base


class JobTypeEnum(str, enum.Enum):
    internship = "internship"
    part_time  = "part_time"
    assistant  = "assistant"


class JobStatusEnum(str, enum.Enum):
    open   = "open"
    closed = "closed"


class Job(Base):
    __tablename__ = "jobs"

    id          = Column(Integer, primary_key=True, index=True)
    employer_id = Column(Integer, ForeignKey("employers.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"))
    title       = Column(String, nullable=False)
    description = Column(String, nullable=False)
    salary      = Column(Float)
    job_type    = Column(Enum(JobTypeEnum), default=JobTypeEnum.internship)
    status      = Column(Enum(JobStatusEnum), default=JobStatusEnum.open)
    deadline    = Column(Date)
    created_at  = Column(DateTime, default=datetime.utcnow)

    employer     = relationship("Employer",     back_populates="jobs")
    category     = relationship("Category",     back_populates="jobs")
    applications = relationship("Application",  back_populates="job")
