"""Выгрузка тренировочных программ в out/data.{json,csv,xml,yaml}.
Запуск из папки src:  python export.py"""
from database.init_db import ensure_db
from services.export_service import export_programs

if __name__ == "__main__":
    ensure_db()
    for path in export_programs():
        print("Создан файл:", path)
