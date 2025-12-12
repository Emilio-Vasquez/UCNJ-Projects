from flask import request, redirect, url_for, flash
from flask_login import login_user
from werkzeug.security import check_password_hash
from .auth import get_user_by_username


def handle_login():
    username = request.form.get("email")
    password = request.form.get("password")
    remember = request.form.get("remember") == "on"

    # Optional but good practice: validate input
    if not username or not password:
        flash("Please enter both username and password.")
        return redirect(url_for("login_page"))

    # Fetch user from DB
    user = get_user_by_username(username)

    # Authentication
    if user is None or not check_password_hash(user.password_hash, password):
        flash("Invalid username or password")
        return redirect(url_for("login_page"))

    # Log them in
    login_user(user, remember=remember)
    return redirect(url_for("index"))
