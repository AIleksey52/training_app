"""Учёт тренировочных программ — точка входа (ЛР №4).
Запуск из папки src:  python main.py
Пересоздать БД с тестовыми данными:  python -m database.init_db
"""
import sys

# Windows: принудительно UTF-8, чтобы русский текст не превращался в «����»
for stream in (sys.stdin, sys.stdout, sys.stderr):
    try:
        stream.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

from config import TRAINER_ROLE_ID
from database.init_db import ensure_db
from ui import auth
from ui.athlete_menu import athlete_menu
from ui.trainer_menu import trainer_menu


def main():
    ensure_db()
    while True:
        print("\n===== Учёт тренировочных программ =====")
        print("1. Вход")
        print("2. Регистрация")
        print("0. Выход")
        choice = input("Выберите действие: ").strip()
        if choice == "1":
            user = auth.login()
            if user:
                if user.role_id == TRAINER_ROLE_ID:
                    trainer_menu(user)
                else:
                    athlete_menu(user)
        elif choice == "2":
            auth.register()
        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Нет такого пункта")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход.")
