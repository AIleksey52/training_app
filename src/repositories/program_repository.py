from database.database import get_connection
from models.program import Program

_SELECT = """
    SELECT p.program_id, p.name, p.description, p.duration_weeks,
           p.level_id, p.trainer_id, l.name, u.full_name
    FROM programs p
    JOIN difficulty_levels l ON l.level_id = p.level_id
    JOIN users u ON u.user_id = p.trainer_id
"""


def _map(row) -> Program:
    return Program(*row)


def create(name: str, description: str | None, duration_weeks: int,
           level_id: int, trainer_id: int) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO programs (name, description, duration_weeks, level_id, trainer_id)
        VALUES (?, ?, ?, ?, ?)
    """, (name, description, duration_weeks, level_id, trainer_id))
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id


def get_by_id(program_id: int) -> Program | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(_SELECT + " WHERE p.program_id = ?", (program_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None


def get_all() -> list[Program]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(_SELECT + " ORDER BY p.level_id, p.name")
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]


def get_by_level(level_id: int) -> list[Program]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(_SELECT + " WHERE p.level_id = ? ORDER BY p.name", (level_id,))
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]


def search_by_name(text: str) -> list[Program]:
    # lower() в SQLite не работает с кириллицей, поэтому фильтр по подстроке делаем в Python
    return [p for p in get_all() if text.lower() in p.name.lower()]


def get_by_trainer(trainer_id: int) -> list[Program]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(_SELECT + " WHERE p.trainer_id = ? ORDER BY p.name", (trainer_id,))
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]


def update(program_id: int, name: str, description: str | None,
           duration_weeks: int, level_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE programs
        SET name = ?, description = ?, duration_weeks = ?, level_id = ?
        WHERE program_id = ?
    """, (name, description, duration_weeks, level_id, program_id))
    conn.commit()
    conn.close()


def delete(program_id: int):
    # упражнения программы удалятся каскадно (ON DELETE CASCADE)
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM programs WHERE program_id = ?", (program_id,))
    conn.commit()
    conn.close()
