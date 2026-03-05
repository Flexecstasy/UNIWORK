from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from app.database import get_db
from app.core.security import get_current_user
from app.core.errors import AppError
from app.models.user import User
from app.models.notification import Notification

router = APIRouter(prefix="/api/users", tags=["Users"])


class NotificationOut(BaseModel):
    id:      int
    text:    str
    is_read: bool

    model_config = {"from_attributes": True}


@router.get("/notifications", response_model=List[NotificationOut],
            summary="Мои уведомления")
def get_notifications(
    db:   Session = Depends(get_db),
    user: User    = Depends(get_current_user),
):
    notifs = db.query(Notification).filter(Notification.user_id == user.id).all()
    for n in notifs:
        n.is_read = True
    db.commit()
    return notifs
