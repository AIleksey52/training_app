from pathlib import Path

from database.database import DB_PATH, get_connection

SCHEMA_PATH = Path(__file__).parent / "schema.sql"


def init_db():
    """Создаёт таблицы и заполняет их тестовыми данными (пересоздаёт БД)."""
    conn = get_connection()
    with open(SCHEMA_PATH, encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
    print("База данных создана:", DB_PATH)


def ensure_db():
    """Создаёт БД, если файла ещё нет."""
    if not DB_PATH.exists():
        init_db()


if __name__ == "__main__":
    init_db()
