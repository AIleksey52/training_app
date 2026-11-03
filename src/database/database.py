import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "training.db"


def get_connection() -> sqlite3.Connection:
    """Возвращает подключение к БД с включённой проверкой внешних ключей."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
