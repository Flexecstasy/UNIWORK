from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}  # только для SQLite
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def init_db():
    """Initialize database tables"""
    # Import all models here to ensure they are registered with Base
    from app.models.user import User
    from app.models.student import Student
    from app.models.employer import Employer
    from app.models.category import Category
    from app.models.job import Job
    from app.models.application import Application
    from app.models.resume import Resume
    from app.models.review import Review
    from app.models.message import Message
    from app.models.notification import Notification
    
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
