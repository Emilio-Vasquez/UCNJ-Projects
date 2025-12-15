
from flask import session
from werkzeug.security import check_password_hash
from app.db import get_db

def handle_login(email, password):
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute(
        "SELECT id, username, email, password_hash, is_verified FROM users WHERE email = %s",
        (email,),
    )
    user = cur.fetchone()
    cur.close()

    if not user:
        return False, "Invalid email or password."

    if not check_password_hash(user["password_hash"], password):
        return False, "Invalid email or password."

    # if you want to skip verification for now, comment this block:
    # if not user["is_verified"]:
    #     return False, "Please verify your email before logging in."

    session["user_id"] = user["id"]
    session["username"] = user["username"]

    return True, "Login successful."
