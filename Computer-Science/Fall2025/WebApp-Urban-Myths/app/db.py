"""
db.py
Handles all MySQL database connections, cleanup, and simple query testing.

Why this file matters:
1. Centralizes connection logic.
2. Any route/file can call get_db() to access MySQL.
3. Ensures connections open *and close properly* for every request.
"""

import mysql.connector
from mysql.connector import Error
from flask import current_app, g
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# ---------------------------------------
# Get Database Connection
# ---------------------------------------
def get_db():
    """
    Opens a MySQL connection and stores it in g.db for the current request.
    If the connection fails, returns None instead of crashing the app.
    """
    if "db" not in g:
        try:
            g.db = mysql.connector.connect(
                host = current_app.config.get("DB_HOST"),
                port=current_app.config["DB_PORT"],
                user=current_app.config["DB_USER"],
                password=current_app.config["DB_PASSWORD"],
                database=current_app.config["DB_NAME"],
            )
        except Error as e:
            print("MySQL connection error:", e)
            g.db = None

    return g.db


# ---------------------------------------
# Close Database Connection
# ---------------------------------------
def close_db(e=None):
    """
    Closes the database connection at the end of the request.
    Flask will automatically call this because init_app() registers it.
    """
    db = g.pop("db", None)
    if db is not None:
        db.close()


# ---------------------------------------
# Flask Integration
# ---------------------------------------
def init_app(app):
    """
    Registers the database cleanup function with Flask.
    This ensures each request opens & closes the DB properly.
    """
    app.teardown_appcontext(close_db)


# ---------------------------------------
# Simple Query Test Helper
# ---------------------------------------
def query_test(sql, params=()):
    """
    Runs a simple SELECT query.
    Returns True if a row exists, False otherwise.

    If DB connection failed, returns False.
    """
    conn = get_db()
    if conn is None:
        return False

    with conn.cursor(dictionary=True) as cur:
        cur.execute(sql, params)
        row = cur.fetchone()
        return True if row else False
    
class Myth(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    short_description = db.Column(db.String(255), nullable=False)
    full_story = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(100))
    image_url = db.Column(db.String(255))
    price = db.Column(db.Integer, nullable=False)