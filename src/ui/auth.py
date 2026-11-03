from getpass import getpass

from services import auth_service
from services.errors import ServiceError
from ui.helpers import ask


def _read_password(prompt: str) -> str:
    try:
        return getpass(f"{prompt} (ввод скрыт): ")
    except Exception:  # некоторые консоли IDE не поддерживают скрытый ввод
        return input(f"{prompt}: ")


def login():
    login_value = ask("Логин")
    password_value = _read_password("Пароль")
    user = auth_service.authenticate(login_value, password_value)
    if not user:
        print("Неверный логин или пароль")
        return None
    print(f"Добро пожаловать, {user.full_name} ({user.role_name})!")
    return user


def _read_new_user():
    return (ask("Логин (латиница)"), ask("ФИО"),
            _read_password("Пароль (не короче 6 символов)"), _read_password("Повторите пароль"))


def register():
    print("\n--- Регистрация спортсмена ---")
    try:
        user = auth_service.register_athlete(*_read_new_user())
        print(f"Готово! Вы зарегистрированы как {user.login}. Теперь войдите в систему.")
    except ServiceError as e:
        print(f"Ошибка: {e}")


def add_trainer(current_user):
    print("\n--- Добавление тренера ---")
    try:
        user = auth_service.create_trainer(current_user, *_read_new_user())
        print(f"Тренер {user.full_name} добавлен.")
    except ServiceError as e:
        print(f"Ошибка: {e}")


def change_password(current_user):
    try:
        auth_service.change_password(current_user, _read_password("Текущий пароль"),
                                     _read_password("Новый пароль"),
                                     _read_password("Повторите новый пароль"))
        print("Пароль изменён.")
    except ServiceError as e:
        print(f"Ошибка: {e}")
