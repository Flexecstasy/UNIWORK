from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from datetime import date, timedelta

from app.database import init_db, SessionLocal
from app.core.errors import (
    AppError,
    app_error_handler,
    http_exception_handler,
    validation_exception_handler,
    generic_exception_handler,
)
from app.core.security import hash_password
from app.routers import auth, jobs, applications, categories, users
from app.models.category import Category
from app.models.user import User, RoleEnum
from app.models.employer import Employer
from app.models.job import Job, JobTypeEnum


# ─── Приложение ───────────────────────────────────────────────────────────────

app = FastAPI(
    title="UniWork API",
    description="Платформа для поиска временной работы и стажировок в кампусе",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ─── CORS (чтобы фронтенд мог обращаться к API) ──────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Обработчики ошибок ───────────────────────────────────────────────────────

app.add_exception_handler(AppError,                  app_error_handler)
app.add_exception_handler(StarletteHTTPException,    http_exception_handler)
app.add_exception_handler(RequestValidationError,    validation_exception_handler)
app.add_exception_handler(Exception,                 generic_exception_handler)

# ─── Роутеры ──────────────────────────────────────────────────────────────────

app.include_router(auth.router)
app.include_router(jobs.router)
app.include_router(applications.router)
app.include_router(categories.router)
app.include_router(users.router)


# ─── Старт: создать таблицы + сид категорий ──────────────────────────────────

@app.on_event("startup")
def on_startup():
    init_db()
    db = SessionLocal()
    try:
        # Сид категорий
        if db.query(Category).count() == 0:
            seed_categories = [
                Category(name="ИТ и разработка",      icon="laptop"),
                Category(name="Наука и исследования", icon="flask"),
                Category(name="Администрация",        icon="building"),
                Category(name="Образование",          icon="book"),
                Category(name="Медиа и дизайн",       icon="palette"),
            ]
            db.add_all(seed_categories)

        # Сид демо‑работодателя и нескольких вакансий
        if db.query(Job).count() == 0:
            demo_email = "employer@uniwork.kz"
            employer_user = db.query(User).filter(User.email == demo_email).first()
            if not employer_user:
                employer_user = User(
                    email=demo_email,
                    hashed_password=hash_password("employer123"),
                    role=RoleEnum.employer,
                )
                db.add(employer_user)
                db.flush()

            employer = employer_user.employer
            if not employer:
                employer = Employer(
                    user_id=employer_user.id,
                    organization_name="Кафедра информатики",
                    contact_person="Иван Петров",
                )
                db.add(employer)
                db.flush()

            categories = {c.name: c.id for c in db.query(Category).all()}
            today = date.today()

            demo_jobs = [
                Job(
                    title="Ассистент кафедры информатики",
                    description="Помощь преподавателям в проведении лабораторных работ, проверка заданий студентов, подготовка материалов.",
                    salary=60000,
                    job_type=JobTypeEnum.assistant,
                    employer_id=employer.id,
                    category_id=categories.get("ИТ и разработка"),
                    deadline=today + timedelta(days=30),
                ),
                Job(
                    title="Стажёр в научной лаборатории",
                    description="Участие в экспериментальных исследованиях, обработка данных, подготовка отчётов по результатам.",
                    salary=80000,
                    job_type=JobTypeEnum.internship,
                    employer_id=employer.id,
                    category_id=categories.get("Наука и исследования"),
                    deadline=today + timedelta(days=45),
                ),
                Job(
                    title="Администратор студенческого офиса",
                    description="Консультация студентов, работа с обращениями, помощь в организации мероприятий.",
                    salary=50000,
                    job_type=JobTypeEnum.part_time,
                    employer_id=employer.id,
                    category_id=categories.get("Администрация"),
                    deadline=today + timedelta(days=20),
                ),
            ]
            db.add_all(demo_jobs)

        db.commit()
    finally:
        db.close()


@app.get("/", tags=["Root"])
def root():
    return {"message": "UniWork API запущен. Документация: /docs"}
