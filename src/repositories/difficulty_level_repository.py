from database.database import get_connection
from models.difficulty_level import DifficultyLevel


def _map(row) -> DifficultyLevel:
    return DifficultyLevel(*row)


def get_all() -> list[DifficultyLevel]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT level_id, name FROM difficulty_levels ORDER BY level_id")
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]


def get_by_id(level_id: int) -> DifficultyLevel | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT level_id, name FROM difficulty_levels WHERE level_id = ?", (level_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None
