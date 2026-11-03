from database.database import get_connection
from models.program_exercise import ProgramExercise

_SELECT = """
    SELECT pe.id, pe.program_id, pe.exercise_id, pe.position,
           pe.sets, pe.reps, pe.rest_seconds, e.name
    FROM program_exercises pe
    JOIN exercises e ON e.exercise_id = pe.exercise_id
"""


def _map(row) -> ProgramExercise:
    return ProgramExercise(*row)


def create(program_id: int, exercise_id: int, position: int,
           sets: int, reps: int, rest_seconds: int) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO program_exercises (program_id, exercise_id, position, sets, reps, rest_seconds)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (program_id, exercise_id, position, sets, reps, rest_seconds))
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id


def get_by_id(item_id: int) -> ProgramExercise | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(_SELECT + " WHERE pe.id = ?", (item_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None


def get_by_program(program_id: int) -> list[ProgramExercise]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(_SELECT + " WHERE pe.program_id = ? ORDER BY pe.position", (program_id,))
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]


def get_next_position(program_id: int) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COALESCE(MAX(position), 0) + 1 FROM program_exercises WHERE program_id = ?",
                (program_id,))
    pos = cur.fetchone()[0]
    conn.close()
    return pos


def count_by_exercise(exercise_id: int) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM program_exercises WHERE exercise_id = ?", (exercise_id,))
    count = cur.fetchone()[0]
    conn.close()
    return count


def update(item_id: int, sets: int, reps: int, rest_seconds: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE program_exercises
        SET sets = ?, reps = ?, rest_seconds = ?
        WHERE id = ?
    """, (sets, reps, rest_seconds, item_id))
    conn.commit()
    conn.close()


def delete(item_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM program_exercises WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
