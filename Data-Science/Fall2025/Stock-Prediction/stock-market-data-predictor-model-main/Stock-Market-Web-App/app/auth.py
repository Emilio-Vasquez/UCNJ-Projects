from .db import get_db
from werkzeug.security import check_password_hash


class UserObj:
    """Lightweight object for Flask-Login."""

    def __init__(self, id, name, email, password_hash):
        self.id = id
        self.name = name
        self.email = email
        self.password_hash = password_hash

    def get_id(self):
        return str(self.id)

    # Flask-Login required attributes
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    # Needed for login authentication
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


def user_exists(email):
    sql = "SELECT id FROM users WHERE email = %s LIMIT 1"
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute(sql, (email,))
        return cur.fetchone() is not None


def insert_user(name, email, password_hash):
    sql = """
        INSERT INTO users (name, email, password_hash)
        VALUES (%s, %s, %s)
    """
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (name, email, password_hash))
        conn.commit()
        return True
    except Exception:
        conn.rollback()
        return False


def get_user_by_email(email):
    sql = "SELECT id, name, email, password_hash FROM users WHERE email = %s LIMIT 1"
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute(sql, (email,))
        row = cur.fetchone()
        if row:
            return UserObj(*row)
        return None


def get_user_by_username(username):
    sql = """
        SELECT id, username, email, password_hash
        FROM users
        WHERE username = %s
        LIMIT 1
    """
    conn = get_db()

    with conn.cursor() as cur:
        cur.execute(sql, (username,))
        row = cur.fetchone()
        if row:
            return UserObj(*row)
        return None


def get_user_by_id(id):
    sql = "SELECT id, name, email, password_hash FROM users WHERE id = %s LIMIT 1"
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute(sql, (id,))
        row = cur.fetchone()
        if row:
            return UserObj(*row)
        return None
