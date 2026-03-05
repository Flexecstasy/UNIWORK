from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.database import init_db
from app.core.errors import (
    AppError,
    app_error_handler,
    http_exception_handler,
    validation_exception_handler,
    generic_exception_handler,
)
from app.routers import auth, jobs, applications, categories, users
from app.models.category import Category
from app.database import SessionLocal


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
    if db.query(Category).count() == 0:
        seed = [
            Category(name="ИТ и разработка",      icon="laptop"),
            Category(name="Наука и исследования",  icon="flask"),
            Category(name="Администрация",         icon="building"),
            Category(name="Образование",           icon="book"),
            Category(name="Медиа и дизайн",        icon="palette"),
        ]
        db.add_all(seed)
        db.commit()
    db.close()


@app.get("/", tags=["Root"])
def root():
    return {"message": "UniWork API запущен. Документация: /docs"}
