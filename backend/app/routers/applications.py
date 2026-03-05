from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.application import ApplicationCreate, ApplicationStatusUpdate, ApplicationOut
from app.crud import applications as crud
from app.core.security import get_current_user
from app.core.errors import AppError
from app.models.user import User, RoleEnum

router = APIRouter(prefix="/api/applications", tags=["Applications"])


@router.post("/", response_model=ApplicationOut, status_code=201,
             summary="Подать заявку на вакансию (студент)")
def apply(
    data: ApplicationCreate,
    db:   Session = Depends(get_db),
    user: User    = Depends(get_current_user),
):
    if user.role != RoleEnum.student:
        raise AppError(403, "FORBIDDEN", "Только студент может подавать заявки")
    return crud.create_application(db, data, student_id=user.student.id)


@router.get("/my", response_model=List[ApplicationOut],
            summary="Мои заявки (студент)")
def my_applications(
    db:   Session = Depends(get_db),
    user: User    = Depends(get_current_user),
):
    if user.role != RoleEnum.student:
        raise AppError(403, "FORBIDDEN", "Только студент может просматривать свои заявки")
    return crud.get_student_applications(db, student_id=user.student.id)


@router.get("/job/{job_id}", response_model=List[ApplicationOut],
            summary="Заявки на вакансию (работодатель)")
def job_applications(
    job_id: int,
    db:     Session = Depends(get_db),
    user:   User    = Depends(get_current_user),
):
    if user.role != RoleEnum.employer:
        raise AppError(403, "FORBIDDEN", "Только работодатель может просматривать заявки на вакансию")
    return crud.get_job_applications(db, job_id=job_id)


@router.patch("/{app_id}/status", response_model=ApplicationOut,
              summary="Изменить статус заявки (работодатель)")
def update_status(
    app_id: int,
    data:   ApplicationStatusUpdate,
    db:     Session = Depends(get_db),
    user:   User    = Depends(get_current_user),
):
    if user.role != RoleEnum.employer:
        raise AppError(403, "FORBIDDEN", "Только работодатель может менять статус заявки")
    result = crud.update_status(db, app_id, data.status)
    if not result:
        raise AppError(404, "APP_NOT_FOUND", f"Заявка с id={app_id} не найдена")
    return result
