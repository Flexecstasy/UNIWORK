from sqlalchemy.orm import Session
from app.models.job import Job, JobStatusEnum
from app.schemas.job import JobCreate


def get_jobs(db: Session, category_id: int = None, job_type: str = None, search: str = None):
    q = db.query(Job).filter(Job.status == JobStatusEnum.open)
    if category_id:
        q = q.filter(Job.category_id == category_id)
    if job_type:
        q = q.filter(Job.job_type == job_type)
    if search:
        q = q.filter(Job.title.ilike(f"%{search}%"))
    return q.order_by(Job.created_at.desc()).all()


def get_job(db: Session, job_id: int):
    return db.query(Job).filter(Job.id == job_id).first()


def create_job(db: Session, data: JobCreate, employer_id: int):
    job = Job(**data.model_dump(), employer_id=employer_id)
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


def close_job(db: Session, job_id: int):
    job = db.query(Job).filter(Job.id == job_id).first()
    if job:
        job.status = JobStatusEnum.closed
        db.commit()
        db.refresh(job)
    return job
