from dataclasses import dataclass


@dataclass
class User:
    user_id: int
    login: str
    full_name: str
    password_hash: str
    role_id: int
    role_name: str | None = None  # служебное поле: название роли (JOIN с user_roles)
