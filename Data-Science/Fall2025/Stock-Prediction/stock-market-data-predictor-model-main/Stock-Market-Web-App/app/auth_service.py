from werkzeug.security import generate_password_hash
from .auth import user_exists, insert_user


def create_user(name, email, password):
    if user_exists(email):
        return None, "A user already exists with that email address."

    hashed = generate_password_hash(password)
    ok = insert_user(name, email, hashed)

    if not ok:
        return None, "Error creating your account."

    return True, None
