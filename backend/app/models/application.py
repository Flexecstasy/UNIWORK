from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base


class AppStatusEnum(str, enum.Enum):
    pending  = "pending"
    accepted = "accepted"
    rejected = "rejected"


class Application(Base):
    __tablename__ = "applications"

    id         = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    job_id     = Column(Integer, ForeignKey("jobs.id"),     nullable=False)
    resume_id  = Column(Integer, ForeignKey("resumes.id"))
    cover      = Column(String)   # сопроводительное письмо
    status     = Column(Enum(AppStatusEnum), default=AppStatusEnum.pending)
    created_at = Column(DateTime, default=datetime.utcnow)

    student = relationship("Student", back_populates="applications")
    job     = relationship("Job",     back_populates="applications")
