import hashlib

from config import ATHLETE_ROLE_ID, TRAINER_ROLE_ID
from models.user import User
from repositories import user_repository
from services.errors import ServiceError
from services.validators import require_login, require_password, require_text


def hash_password(password: str) -> str:
    """Пароли не храним в открытом виде — только SHA-256 хэш."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def authenticate(login: str, password: str) -> User | None:
    user = user_repository.get_by_login((login or "").strip())
    if user and user.password_hash == hash_password(password or ""):
        return user
    return None


def _create_user(login, full_name, password, password_repeat, role_id) -> User:
    login = require_login(login)
    full_name = require_text(full_name, "ФИО")
    password = require_password(password, password_repeat)
    if user_repository.get_by_login(login):
        raise ServiceError("Пользователь с таким логином уже существует")
    user_id = user_repository.create(login, full_name, hash_password(password), role_id)
    return user_repository.get_by_id(user_id)


def register_athlete(login, full_name, password, password_repeat) -> User:
    """Самостоятельная регистрация — только в роли спортсмена."""
    return _create_user(login, full_name, password, password_repeat, ATHLETE_ROLE_ID)


def create_trainer(current_user: User, login, full_name, password, password_repeat) -> User:
    """Нового тренера (администратора) может добавить только тренер."""
    if current_user.role_id != TRAINER_ROLE_ID:
        raise ServiceError("Добавлять тренеров может только тренер")
    return _create_user(login, full_name, password, password_repeat, TRAINER_ROLE_ID)


def change_password(user: User, old_password, new_password, new_password_repeat):
    if user.password_hash != hash_password(old_password or ""):
        raise ServiceError("Неверный текущий пароль")
    new_password = require_password(new_password, new_password_repeat)
    user_repository.update_password(user.user_id, hash_password(new_password))
    user.password_hash = hash_password(new_password)
