from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.job import JobCreate, JobOut
from app.crud import jobs as crud
from app.core.security import get_current_user
from app.core.errors import AppError
from app.models.user import User, RoleEnum

router = APIRouter(prefix="/api/jobs", tags=["Jobs"])


@router.get("/", response_model=List[JobOut],
            summary="Список открытых вакансий с фильтрами")
def list_jobs(
    category_id: int    = Query(None, description="Фильтр по категории"),
    job_type:    str    = Query(None, description="Тип: internship | part_time | assistant"),
    search:      str    = Query(None, description="Поиск по названию"),
    db: Session = Depends(get_db),
):
    return crud.get_jobs(db, category_id=category_id, job_type=job_type, search=search)


@router.get("/{job_id}", response_model=JobOut,
            summary="Детальная информация о вакансии")
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = crud.get_job(db, job_id)
    if not job:
        raise AppError(404, "JOB_NOT_FOUND", f"Вакансия с id={job_id} не найдена",
                       fix="Проверьте правильность id вакансии")
    return job


@router.post("/", response_model=JobOut, status_code=201,
             summary="Создание вакансии (только работодатель)")
def create_job(
    data: JobCreate,
    db:   Session = Depends(get_db),
    user: User    = Depends(get_current_user),
):
    if user.role != RoleEnum.employer:
        raise AppError(403, "FORBIDDEN", "Только работодатель может создавать вакансии")
    return crud.create_job(db, data, employer_id=user.employer.id)


@router.patch("/{job_id}/close",
              summary="Закрыть вакансию (только владелец)")
def close_job(
    job_id: int,
    db:     Session = Depends(get_db),
    user:   User    = Depends(get_current_user),
):
    job = crud.get_job(db, job_id)
    if not job:
        raise AppError(404, "JOB_NOT_FOUND", f"Вакансия с id={job_id} не найдена")
    if job.employer_id != user.employer.id:
        raise AppError(403, "FORBIDDEN", "Вы не являетесь владельцем этой вакансии")
    return crud.close_job(db, job_id)
