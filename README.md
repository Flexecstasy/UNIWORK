# UniWork - Платформа поиска работы для студентов



---

##  Старт 

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
# http://127.0.0.1:8000/docs
```

---

---

##  Ключевые Особенности

### Система обработки ошибок

- 7 типов HTTP ошибок (400, 401, 403, 404, 409, 422, 500)
- Структурированные JSON ответы
-  информация об ошибках



### Backend (FastAPI)

- RESTful API на основе FastAPI
- Аутентификация через JWT токены
- SQLAlchemy ORM с SQLite
- Полная Pydantic валидация
- Система логирования и мониторинга

###  Frontend (Vanilla JS)

- Чистый HTML/CSS/JavaScript
- Асинхронные запросы через Fetch API
- Адаптивный дизайн
- Интеграция с REST API


**UniWork** — это веб-платформа, которая связывает студентов с работодателями, предоставляя возможность:

- Студентам найти интересующие их вакансии работы и стажировок
- Подать заявки на позиции с прикреплением резюме
- Оставлять отзывы о работодателях и позициях
- Работодателям размещать вакансии и управлять заявками
- Общаться с кандидатами через встроенную систему сообщений
- Получать уведомления о новых событиях

### Архитектура

Проект разделен на две части:

#### Backend (FastAPI)
- RESTful API на основе **FastAPI**
- Аутентификация через **JWT токены**
- Работа с базой данных **SQLite** (SQLAlchemy ORM)
- Полная валидация данных через **Pydantic**

#### Frontend (Vanilla JavaScript)
- Чистый HTML/CSS/JavaScript (без фреймворков)
- Асинхронные запросы через Fetch API
- Адаптивный дизайн
- Интеграция с REST API

### Структура проекта

```
uniwork/
├── backend/                 # FastAPI приложение
│   ├── app/
│   │   ├── main.py         # Точка входа приложения
│   │   ├── database.py     # Конфигурация БД
│   │   ├── core/
│   │   │   ├── config.py   # Параметры приложения
│   │   │   ├── security.py # JWT и хеширование паролей
│   │   │   └── errors.py   # Обработчики ошибок
│   │   ├── models/         # SQLAlchemy модели
│   │   │   ├── user.py
│   │   │   ├── student.py
│   │   │   ├── employer.py
│   │   │   ├── job.py
│   │   │   ├── application.py
│   │   │   ├── resume.py
│   │   │   ├── review.py
│   │   │   ├── message.py
│   │   │   ├── notification.py
│   │   │   └── category.py
│   │   ├── schemas/        # Pydantic схемы валидации
│   │   ├── routers/        # API маршруты
│   │   └── crud/           # Database операции
│   ├── requirements.txt    # Зависимости
│   └── uniwork.db         # SQLite база данных
│
├── frontend/               # Веб интерфейс
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── job-detail.html
│   ├── apply.html
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── api.js         # Функции для работы с API
│       ├── auth.js        # Аутентификация
│       ├── jobs.js        # Работа с вакансиями
│       └── dashboard.js   # Личный кабинет
│
└── README.md
```

### Установка и запуск

#### Требования
- Python 3.12+
- SQLite (включен в Python)

#### Backend

1. Перейти в директорию backend:
   ```bash
   cd backend
   ```

2. Установить зависимости:
   ```bash
   pip install -r requirements.txt
   ```

3. Запустить сервер:
   ```bash
   python -m uvicorn app.main:app --reload
   ```

   Сервер запустится на `http://127.0.0.1:8000`
   
   API документация:
   - Swagger UI: `http://127.0.0.1:8000/docs`
   - ReDoc: `http://127.0.0.1:8000/redoc`

#### Frontend

1. Запустить локальный сервер (необходимо для CORS):
   
   **Вариант 1: Python (встроенный)**
   ```bash
   cd frontend
   python -m http.server 3000
   ```

   **Вариант 2: Node.js**
   ```bash
   cd frontend
   npx http-server -p 3000
   ```

2. Открыть в браузере:
   ```
   http://localhost:3000
   ```

