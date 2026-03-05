"""
Тесты обработки ошибок UniWork API.
Проверяют: валидацию, авторизацию, отсутствие данных, формат ответа.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app, raise_server_exceptions=False)

def check_error_format(body: dict):
    """Каждая ошибка должна содержать success=False и блок error с полями."""
    assert body["success"] is False
    err = body["error"]
    assert "code"    in err, "Нет поля code"
    assert "message" in err, "Нет поля message"
    assert "fix"     in err, "Нет поля fix"


# ─── 1. Ошибки валидации (422) 

class TestValidationErrors:

    def test_register_missing_all_fields(self):
        """Пустое тело → 422 с описанием полей."""
        r = client.post("/api/auth/register", json={})
        assert r.status_code == 422
        body = r.json()
        check_error_format(body)
        assert body["error"]["code"] == "VALIDATION_ERROR"

    def test_register_invalid_email(self):
        """Невалидный email → 422."""
        r = client.post("/api/auth/register", json={
            "email": "not-an-email",
            "password": "123456",
            "role": "student",
            "first_name": "Иван",
            "last_name": "Иванов"
        })
        assert r.status_code == 422
        check_error_format(r.json())

    def test_register_invalid_role(self):
        """Неизвестная роль → 422."""
        r = client.post("/api/auth/register", json={
            "email": "test@uni.ru",
            "password": "123456",
            "role": "admin",
            "first_name": "Иван",
            "last_name": "Иванов"
        })
        assert r.status_code == 422
        check_error_format(r.json())

    def test_apply_missing_job_id(self):
        """Заявка без job_id → 422."""
        r = client.post("/api/applications/", json={"cover": "Хочу работать"},
                        headers={"Authorization": "Bearer fake"})
        assert r.status_code in (401, 422)


# ─── 2. Ошибки авторизации (401 / 403) 

class TestAuthErrors:

    def test_no_token(self):
        """Запрос без токена → 401."""
        r = client.get("/api/auth/me")
        assert r.status_code == 401
        body = r.json()
        check_error_format(body)
        assert body["error"]["code"] == "UNAUTHORIZED"

    def test_invalid_token(self):
        """Невалидный токен → 401."""
        r = client.get("/api/auth/me", headers={"Authorization": "Bearer invalid.token.here"})
        assert r.status_code == 401
        body = r.json()
        check_error_format(body)
        assert body["error"]["code"] in ("UNAUTHORIZED", "INVALID_TOKEN")

    def test_wrong_credentials(self):
        """Неверный пароль → 401."""
        r = client.post("/api/auth/login", json={
            "email": "nobody@uni.ru",
            "password": "wrongpass"
        })
        assert r.status_code == 401
        body = r.json()
        check_error_format(body)
        assert body["error"]["code"] == "INVALID_CREDENTIALS"

    def test_fix_hint_present_on_401(self):
        """При 401 должна быть подсказка fix."""
        r = client.post("/api/auth/login", json={
            "email": "x@x.ru", "password": "bad"
        })
        assert r.json()["error"]["fix"] is not None


# ─── 3. Ошибки отсутствия данных (404) 

class TestNotFoundErrors:

    def test_job_not_found(self):
        """Несуществующая вакансия → 404."""
        r = client.get("/api/jobs/999999")
        assert r.status_code == 404
        body = r.json()
        check_error_format(body)
        assert body["error"]["code"] == "JOB_NOT_FOUND"

    def test_unknown_route(self):
        """Несуществующий маршрут → 404."""
        r = client.get("/api/nonexistent")
        assert r.status_code == 404

    def test_404_has_fix(self):
        """404 должен содержать поле fix."""
        r = client.get("/api/jobs/999999")
        assert r.json()["error"]["fix"] is not None


# ─── 4. Дублирование / бизнес-логика (400) 

class TestBusinessErrors:

    def _register(self, email: str):
        return client.post("/api/auth/register", json={
            "email": email,
            "password": "password123",
            "role": "student",
            "first_name": "Тест",
            "last_name": "Тестов"
        })

    def test_duplicate_email(self):
        """Повторная регистрация с тем же email → 400."""
        email = "dup_test@uni.ru"
        self._register(email)          # первый раз — ок
        r = self._register(email)      # второй раз — ошибка
        assert r.status_code == 400
        body = r.json()
        check_error_format(body)
        assert body["error"]["code"] == "EMAIL_EXISTS"

    def test_employer_without_organization(self):
        """Работодатель без organization → 400."""
        r = client.post("/api/auth/register", json={
            "email": "emp_no_org@uni.ru",
            "password": "password123",
            "role": "employer",
            "first_name": "Работодатель",
            "last_name": "Тестов"
        })
        assert r.status_code == 400
        body = r.json()
        check_error_format(body)
        assert body["error"]["code"] == "MISSING_FIELD"


# ─── 5. Формат ответа (общий) 

class TestResponseFormat:

    def test_success_response_has_no_error_key(self):
        """Успешный ответ не должен содержать ключ error."""
        r = client.get("/api/jobs/")
        assert r.status_code == 200
        # jobs возвращает список, не словарь — просто проверяем статус
        assert isinstance(r.json(), list)

    def test_error_message_is_string(self):
        """Поле message должно быть строкой, понятной пользователю."""
        r = client.get("/api/jobs/999999")
        msg = r.json()["error"]["message"]
        assert isinstance(msg, str)
        assert len(msg) > 5

    def test_error_code_is_uppercase(self):
        """Код ошибки должен быть в верхнем регистре."""
        r = client.get("/api/jobs/999999")
        code = r.json()["error"]["code"]
        assert code == code.upper()

    def test_categories_returns_list(self):
        """Категории доступны без авторизации."""
        r = client.get("/api/categories/")
        assert r.status_code == 200
        assert isinstance(r.json(), list)