from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Resume(Base):
    __tablename__ = "resumes"

    id         = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    title      = Column(String, nullable=False)
    content    = Column(String, nullable=False)   # текстовое содержимое резюме
    created_at = Column(DateTime, default=datetime.utcnow)

    student = relationship("Student")
