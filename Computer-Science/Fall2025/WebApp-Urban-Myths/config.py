import os
from pathlib import Path
from dotenv import load_dotenv

"""
This is the config.py script.

This script will call load_dotenv() to extract environment variables
Then we set up our application's configuration values.

The keys we will call:
- Flask's secret key: SECRET_KEY
- Database connection values:
    - DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME
"""

# Load variables from .env into OS environment
load_dotenv()

class Config:
    """This is the configuration object."""

    # Base directory of project
    BASE_DIR = Path(__file__).resolve().parent

    # Flask Security
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")
    SECURITY_PASSWORD_SALT = os.getenv("SECURITY_PASSWORD_SALT", "dev-salt-change-me")

    # --- DATABASE CONFIG ---
    # Try to load from .env — if missing, fall back to hardcoded defaults
    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT = int(os.getenv("DB_PORT", 3306))
    DB_USER = os.getenv("DB_USER", "flaskuser")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "password123")
    DB_NAME = os.getenv("DB_NAME", "urban_myths_db")

    # --- EMAIL (GMAIL SMTP) CONFIG ---
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True

    # Default to Gmail credentials (but allow overriding with .env)
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
