"""
This is the db.py script

This scrip will be responsible for connecting to your MySQL database and cleaning it up properly

Centralized connection logic, call this script to access database
"""

import mysql.connector #Driver for MySQL
from flask import current_app, g # current app gives use the configurations we need from the config.py script
# g stores per request data that we get back from config call

def get_db():
    """"
    Opens up sql connection and sends it to python
    """
    if "db" not in g:
        g.db = mysql.connector.connect(
            host = current_app.config['DB_HOST'],
            port = current_app.config['DB_PORT'],
            user = current_app.config['DB_USER'],
            password = current_app.config['DB_PASSWORD'],
            database = current_app.config['DB_NAME']
        )
    return g.db

def close_db(e=None):
    """"
    This function closes the database connection
    """
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_app(app):
    """
    This registers close_db()
    """
    app.teardown_appcontext(close_db) #calling close_db()

#sql test
def query_test(sql, params=()):
    """"
    Run a select query
    """
    conn = get_db()
    with conn.cursor(dictionary=True) as cur:
        cur.execute(sql, params)
        row = cur.fetchone()
        return True if row else False