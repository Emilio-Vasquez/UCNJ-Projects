from flask import redirect
from .db import get_db

def handle_feedback(request):
    """
    Handles feedback form submission and stores it in MySQL.
    """
    # Get form data
    date = request.form.get("date") or None ## or none bc not required
    email = request.form.get("email") or None ## stores as null ^^
    comment = request.form.get("comment")

    # Connect to DB so feedback can be stored
    db = get_db()
    cursor = db.cursor()

    # insert feedback into database
    sql = """
        INSERT INTO feedback (date, email, comment)
        VALUES (%s, %s, %s)
    """
    cursor.execute(sql, (date, email, comment))
    db.commit()
    cursor.close()

    # back home after submitting feedback form
    return redirect("/")