from database.database import get_connection
from models.user_role import UserRole


def _map(row) -> UserRole:
    return UserRole(*row)


def get_all() -> list[UserRole]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT role_id, name FROM user_roles ORDER BY role_id")
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]


def get_by_id(role_id: int) -> UserRole | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT role_id, name FROM user_roles WHERE role_id = ?", (role_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None
