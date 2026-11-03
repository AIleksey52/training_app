from database.database import get_connection
from models.user import User

_SELECT = """
    SELECT u.user_id, u.login, u.full_name, u.password_hash, u.role_id, r.name
    FROM users u
    JOIN user_roles r ON r.role_id = u.role_id
"""


def _map(row) -> User:
    return User(*row)


def create(login: str, full_name: str, password_hash: str, role_id: int) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO users (login, full_name, password_hash, role_id)
        VALUES (?, ?, ?, ?)
    """, (login, full_name, password_hash, role_id))
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id


def get_by_id(user_id: int) -> User | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(_SELECT + " WHERE u.user_id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None


def get_by_login(login: str) -> User | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(_SELECT + " WHERE lower(u.login) = lower(?)", (login,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None


def get_all() -> list[User]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(_SELECT + " ORDER BY u.role_id, u.full_name")
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]


def update_full_name(user_id: int, full_name: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET full_name = ? WHERE user_id = ?", (full_name, user_id))
    conn.commit()
    conn.close()


def update_password(user_id: int, password_hash: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET password_hash = ? WHERE user_id = ?", (password_hash, user_id))
    conn.commit()
    conn.close()


def delete(user_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()
