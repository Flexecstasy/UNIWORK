from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException


class AppError(Exception):
    """Custom application error"""
    def __init__(self, status_code: int, error_code: str, message: str, fix: str = None, detail: str = None, fields: dict = None):
        self.status_code = status_code
        self.error_code = error_code
        self.message = message
        self.fix = fix
        self.detail = detail
        self.fields = fields
        super().__init__(message)


def error_response(status_code: int, code: str, message: str, fix: str = None, detail: str = None, fields: dict = None):
    """Create standardized error response with success=False"""
    error_body = {
        "code": code,
        "message": message,
    }
    if fix:
        error_body["fix"] = fix
    if detail:
        error_body["detail"] = detail
    
    body = {
        "success": False,
        "error": error_body,
    }
    if fields:
        body["error"]["fields"] = fields
    
    return JSONResponse(status_code=status_code, content=body)


async def app_error_handler(request: Request, exc: AppError):
    return error_response(
        status_code=exc.status_code,
        code=exc.error_code,
        message=exc.message,
        fix=exc.fix,
        detail=exc.detail,
        fields=exc.fields,
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    error_codes = {
        400: ("BAD_REQUEST", "Некорректный запрос. Проверьте переданные данные.", "Проверьте синтаксис запроса и типы данных."),
        401: ("UNAUTHORIZED", "Необходима авторизация. Передайте корректный токен.", "Войдите в систему и повторите запрос."),
        403: ("FORBIDDEN", "Доступ запрещён. У вас нет прав на это действие.", "Проверьте свои права доступа."),
        404: ("NOT_FOUND", "Запрашиваемый ресурс не найден.", "Проверьте правильность идентификатора ресурса."),
        409: ("CONFLICT", "Конфликт данных. Ресурс уже существует.", "Проверьте уникальность ключевых полей."),
        500: ("INTERNAL_ERROR", "Внутренняя ошибка сервера. Попробуйте позже.", "Свяжитесь с поддержкой если ошибка повторяется."),
    }
    code, message, fix = error_codes.get(exc.status_code, ("ERROR", str(exc.detail), "Повторите операцию позже."))
    return error_response(
        status_code=exc.status_code,
        code=code,
        message=message,
        fix=fix,
        detail=str(exc.detail) if exc.detail else None,
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    fields = {}
    for err in exc.errors():
        field = ".".join(str(e) for e in err["loc"] if e != "body")
        fields[field] = {
            "message": err["msg"],
            "fix": f"Поле '{field}': {err['msg']}. Тип: {err['type']}",
        }
    return error_response(
        status_code=422,
        code="VALIDATION_ERROR",
        message="Ошибка валидации данных. Проверьте правильность переданных полей.",
        fix="Проверьте типы и формат всех полей в запросе.",
        fields=fields,
    )


async def generic_exception_handler(request: Request, exc: Exception):
    return error_response(
        status_code=500,
        code="INTERNAL_ERROR",
        message="Неожиданная ошибка сервера.",
        fix="Свяжитесь с поддержкой если ошибка повторяется.",
        detail=str(exc),
    )
