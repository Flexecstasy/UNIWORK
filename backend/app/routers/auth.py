from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import RegisterSchema, LoginSchema, TokenSchema, UserOut
from app.models.user import User
from app.models.student import Student
from app.models.employer import Employer
from app.core.security import hash_password, verify_password, create_access_token, get_current_user
from app.core.errors import AppError

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/register", response_model=UserOut, status_code=201,
             summary="Регистрация нового пользователя")
def register(data: RegisterSchema, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email).first():
        raise AppError(400, "EMAIL_EXISTS", "Пользователь с таким email уже существует",
                       fix="Используйте другой email или войдите в существующий аккаунт")

    user = User(email=data.email, hashed_password=hash_password(data.password), role=data.role)
    db.add(user)
    db.flush()

    if data.role == "student":
        db.add(Student(user_id=user.id, full_name=f"{data.first_name} {data.last_name}",
                       specialty=data.specialty, year=data.year))
    else:
        if not data.organization:
            raise AppError(400, "MISSING_FIELD", "Поле organization обязательно для работодателя",
                           fix="Передайте поле organization в теле запроса")
        db.add(Employer(user_id=user.id, organization_name=data.organization,
                        contact_person=data.contact_name or data.first_name))

    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=TokenSchema,
             summary="Вход и получение JWT-токена")
def login(data: LoginSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password):
        raise AppError(401, "INVALID_CREDENTIALS", "Неверный email или пароль",
                       fix="Проверьте правильность введённых данных")

    token = create_access_token({"sub": user.id, "role": user.role})
    return {"access_token": token}


@router.get("/me", response_model=UserOut,
            summary="Данные текущего пользователя")
def me(user: User = Depends(get_current_user)):
    return user
