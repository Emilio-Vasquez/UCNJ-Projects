from dataclasses import dataclass
from typing import Optional

from werkzeug.security import check_password_hash, generate_password_hash

from app.modules.database import db


@dataclass
class AuthResult:
    success: bool
    user_id: Optional[int] = None
    message: str = ""

def register_user(username: str, plain_password: str) -> AuthResult:
    existing_user = db.get_user_by_username(username)
    if existing_user:
        return AuthResult(success=False, message="Username already taken")

    password_hash = generate_password_hash(plain_password)
    try:
        user_id = db.create_user(username, password_hash)
        return AuthResult(success=True, user_id=user_id, message="User created")
    except ValueError as exc:
        return AuthResult(success=False, message=str(exc))


def authenticate_user(username: str, plain_password: str) -> AuthResult:
    user = db.get_user_by_username(username)
    if not user:
        return AuthResult(success=False, message="Invalid credentials")

    if not check_password_hash(user["password"], plain_password):
        return AuthResult(success=False, message="Invalid credentials")

    return AuthResult(success=True, user_id=user["id"], message="Login successful")
