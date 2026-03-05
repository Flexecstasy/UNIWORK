"""
Pytest configuration and shared fixtures.
Configures the Python path so tests can import from app module.
"""

import sys
import os
from pathlib import Path

# Add parent directory to Python path so imports work
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

# Import all models to ensure they're registered before app creation
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

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal, Base, engine


@pytest.fixture
def client():
    """Provide a TestClient for making requests."""
    return TestClient(app, raise_server_exceptions=False)


@pytest.fixture
def db():
    """Provide a database session for tests."""
    # Create tables
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
        # Clean up after test
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="session", autouse=True)
def init_db():
    """Initialize database before running tests."""
    Base.metadata.create_all(bind=engine)
