import re

from services.errors import ServiceError


def require_text(value: str, field: str, max_len: int = 100) -> str:
    value = (value or "").strip()
    if not value:
        raise ServiceError(f"{field}: поле не может быть пустым")
    if len(value) > max_len:
        raise ServiceError(f"{field}: не длиннее {max_len} символов")
    return value


def optional_text(value: str | None, max_len: int = 500) -> str | None:
    value = (value or "").strip()
    if len(value) > max_len:
        raise ServiceError(f"Описание: не длиннее {max_len} символов")
    return value or None


def require_int(value, field: str, min_value: int, max_value: int) -> int:
    try:
        number = int(value)
    except (TypeError, ValueError):
        raise ServiceError(f"{field}: нужно целое число")
    if not min_value <= number <= max_value:
        raise ServiceError(f"{field}: допустимо от {min_value} до {max_value}")
    return number


def require_login(value: str) -> str:
    value = (value or "").strip()
    if not re.fullmatch(r"[A-Za-z0-9_]{3,20}", value):
        raise ServiceError("Логин: 3–20 символов, латиница, цифры или _")
    return value


def require_password(password: str, password_repeat: str) -> str:
    if len(password or "") < 6:
        raise ServiceError("Пароль должен быть не короче 6 символов")
    if password != password_repeat:
        raise ServiceError("Пароли не совпадают")
    return password
