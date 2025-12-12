from .db import get_db


def insert_feedback(name, email, feedback):
    cur = """
                     INSERT INTO feedback (name, email, feedback)
                     VALUES (%s, %s, %s)
                     """
    return safe_insert(cur, (name, email, feedback))


def safe_insert(sql, params=()):
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params)
        conn.commit()
    except Exception as e:
        conn.rollback()


def handle_feedback(name, email, feedback):
    print(name,email,feedback)
    success = insert_feedback(name, email, feedback)
    return success
