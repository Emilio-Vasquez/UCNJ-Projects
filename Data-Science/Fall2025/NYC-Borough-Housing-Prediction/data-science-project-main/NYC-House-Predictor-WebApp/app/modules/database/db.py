"""Database helper functions for SQLite."""
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, Optional

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATABASE_DIR = PROJECT_ROOT / "database"
DB_PATH = DATABASE_DIR / "db.db"
SCHEMA_PATH = DATABASE_DIR / "schema.sql"


def init_db(schema_path: Optional[Path] = None) -> None:
    """Initialize the database using the schema file. When the schema is updated"""
    schema_file = schema_path or SCHEMA_PATH
    with sqlite3.connect(DB_PATH) as conn, open(schema_file, "r", encoding="utf-8") as schema:
        conn.executescript(schema.read())


@contextmanager
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def create_user(username: str, password_hash: str) -> int:
    """
    Raises:
        ValueError: If the username already exists.
    """
    try:
        with get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password_hash),
            )
            conn.commit()
            return cursor.lastrowid
    except sqlite3.IntegrityError as exc:
        raise ValueError("Username already exists") from exc


def get_user_by_username(username: str) -> Optional[Dict[str, Any]]:
    with get_connection() as conn:
        cursor = conn.execute(
            "SELECT id, username, password FROM users WHERE username = ?",
            (username,),
        )
        row = cursor.fetchone()
        return dict(row) if row else None
        
def create_feedback(user_id: int, content: str) -> int:
    try:
        with get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO feedback (user_id, content) VALUES (?, ?)",
                (user_id, content),
            )
            conn.commit()
            return cursor.lastrowid
    except sqlite3.IntegrityError as exc:
        raise ValueError("User not found or invalid feedback data") from exc

def get_all_feedback():
    with get_connection() as conn:
        cursor = conn.execute("""
            SELECT id, user_id, content, created_at
            FROM feedback
            ORDER BY created_at DESC
        """)
        
        rows = cursor.fetchall()
        return rows

def register_prediction(data: dict) -> int:
    sql = """
        INSERT INTO predictions (
            user_id, borough, zip_code, prop_type, gross_sqft, 
            land_sqft, year_built, estimated_price, range_low, range_high
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    params = (
        data.get('user_id'),
        data.get('borough'),
        data.get('zip_code'),
        data.get('prop_type'),
        data.get('gross_sqft'),
        data.get('land_sqft'),
        data.get('year_built'),
        data.get('estimated_price'),
        data.get('range_low'),
        data.get('range_high')
    )
    
    try:
        with get_connection() as conn:
            cursor = conn.execute(sql, params)
            conn.commit()
            return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        raise ValueError("Could not register prediction due to a database error.") from e

def get_all_history(user_id: int) -> list:

    sql = """
        SELECT 
            borough, zip_code, prop_type, gross_sqft, land_sqft, year_built,
            estimated_price, range_low, range_high, created_at
        FROM predictions
        WHERE user_id = ?
        ORDER BY created_at DESC
    """
    try:
        with get_connection() as conn:
            cursor = conn.execute(sql, (user_id,))
            history = cursor.fetchall()
            return [dict(row) for row in history]
    except sqlite3.Error as e:
        print(f"Database error while fetching history: {e}")
        return []