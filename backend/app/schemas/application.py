from pydantic import BaseModel
from datetime import datetime
from app.models.application import AppStatusEnum


class ApplicationCreate(BaseModel):
    job_id:    int
    resume_id: int | None = None
    cover:     str | None = None


class ApplicationStatusUpdate(BaseModel):
    status: AppStatusEnum


class ApplicationOut(BaseModel):
    id:         int
    job_id:     int
    student_id: int
    status:     AppStatusEnum
    cover:      str | None
    created_at: datetime

    model_config = {"from_attributes": True}
