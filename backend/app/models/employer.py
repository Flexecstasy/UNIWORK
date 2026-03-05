from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Employer(Base):
    __tablename__ = "employers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    organization_name = Column(String, nullable=False)
    department = Column(String)
    contact_person = Column(String)
    phone = Column(String)

    user = relationship("User", back_populates="employer")
    jobs = relationship("Job", back_populates="employer")
