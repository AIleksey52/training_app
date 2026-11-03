from database.database import get_connection
from models.exercise import Exercise


def _map(row) -> Exercise:
    return Exercise(*row)


def create(name: str, description: str | None) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO exercises (name, description) VALUES (?, ?)", (name, description))
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id


def get_by_id(exercise_id: int) -> Exercise | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT exercise_id, name, description FROM exercises WHERE exercise_id = ?",
                (exercise_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None


def get_all() -> list[Exercise]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT exercise_id, name, description FROM exercises ORDER BY name")
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]


def update(exercise_id: int, name: str, description: str | None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE exercises SET name = ?, description = ? WHERE exercise_id = ?",
                (name, description, exercise_id))
    conn.commit()
    conn.close()


def delete(exercise_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM exercises WHERE exercise_id = ?", (exercise_id,))
    conn.commit()
    conn.close()
