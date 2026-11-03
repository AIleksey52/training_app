from config import TRAINER_ROLE_ID
from models.user import User
from repositories import program_repository, user_repository
from services.errors import ServiceError


def get_all_users() -> list[User]:
    return user_repository.get_all()


def delete_user(current_user: User, user_id: int):
    if current_user.role_id != TRAINER_ROLE_ID:
        raise ServiceError("Удалять пользователей может только тренер")
    user = user_repository.get_by_id(user_id)
    if not user:
        raise ServiceError("Пользователь не найден")
    if user.user_id == current_user.user_id:
        raise ServiceError("Нельзя удалить самого себя")
    if program_repository.get_by_trainer(user_id):
        raise ServiceError("У тренера есть программы — сначала удалите их")
    user_repository.delete(user_id)
