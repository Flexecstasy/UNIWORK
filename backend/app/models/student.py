from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    full_name = Column(String, nullable=False)
    specialty = Column(String)
    year = Column(Integer)
    phone = Column(String)

    user = relationship("User", back_populates="student")
    applications = relationship("Application", back_populates="student")
