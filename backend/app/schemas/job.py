from pydantic import BaseModel
from datetime import date, datetime
from app.models.job import JobTypeEnum, JobStatusEnum


class JobCreate(BaseModel):
    title:       str
    description: str
    salary:      float | None = None
    job_type:    JobTypeEnum  = JobTypeEnum.internship
    category_id: int | None  = None
    deadline:    date | None = None


class JobOut(BaseModel):
    id:           int
    title:        str
    description:  str
    salary:       float | None
    job_type:     JobTypeEnum
    status:       JobStatusEnum
    deadline:     date | None
    created_at:   datetime
    employer_id:  int
    category_id:  int | None

    model_config = {"from_attributes": True}
