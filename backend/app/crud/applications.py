from sqlalchemy.orm import Session
from app.models.application import Application, AppStatusEnum
from app.models.notification import Notification
from app.schemas.application import ApplicationCreate


def create_application(db: Session, data: ApplicationCreate, student_id: int):
    app = Application(**data.model_dump(), student_id=student_id)
    db.add(app)
    db.commit()
    db.refresh(app)
    return app


def get_student_applications(db: Session, student_id: int):
    return db.query(Application).filter(Application.student_id == student_id).all()


def get_job_applications(db: Session, job_id: int):
    return db.query(Application).filter(Application.job_id == job_id).all()


def update_status(db: Session, app_id: int, status: AppStatusEnum):
    app = db.query(Application).filter(Application.id == app_id).first()
    if app:
        app.status = status
        # уведомление студенту
        label = {"accepted": "принята ✅", "rejected": "отклонена ❌"}.get(status, status)
        notif = Notification(
            user_id=app.student.user_id,
            text=f"Ваша заявка на вакансию #{app.job_id} {label}",
        )
        db.add(notif)
        db.commit()
        db.refresh(app)
    return app
