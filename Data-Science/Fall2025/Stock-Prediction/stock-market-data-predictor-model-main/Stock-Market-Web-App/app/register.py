from flask import request, redirect, url_for, flash
from flask_login import login_user
from .auth_service import create_user
from .auth import get_user_by_email


def handle_registration():
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")

    # Validation (optional but recommended)
    if not name or not email or not password:
        flash("All fields are required.")
        return redirect(url_for("main.signup"))

    # Try to create the user
    success, error = create_user(name, email, password)

    if success:
        user = get_user_by_email(email)
        if user:
            login_user(user)
            return redirect(url_for("main.dashboard"))

        # fallback (should never happen)
        flash("User created but could not log in.")
        return redirect(url_for("main.login"))

    # If creation failed
    flash(error)
    return redirect(url_for("main.signup"))
