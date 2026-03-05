from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Review(Base):
    __tablename__ = "reviews"

    id          = Column(Integer, primary_key=True, index=True)
    student_id  = Column(Integer, ForeignKey("students.id"),  nullable=False)
    employer_id = Column(Integer, ForeignKey("employers.id"), nullable=False)
    rating      = Column(Integer, nullable=False)   # 1-5
    text        = Column(String)
    created_at  = Column(DateTime, default=datetime.utcnow)

    student  = relationship("Student")
    employer = relationship("Employer")
