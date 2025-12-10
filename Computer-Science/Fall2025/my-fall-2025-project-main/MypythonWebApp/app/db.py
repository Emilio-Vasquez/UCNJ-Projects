"""
this is the db.py scr
this script will set up the database connection
1st: its becauase it gives us a connection object
2nd: it will give us a cursor object
    - connection object: this is the object that connects to the database
    - cursor object: this is the object that allows us to execute sql queries
    - we will use pymysql library to connect to mysql database      

"""


import mysql.connector   ## this is the driver for mysql, its important to connect to python
from flask import current_app, g  ## g is a global object that is unique for each request. it is used to store data that can be accessed by other functions during the request. current_app is used to access the application context

def get_db():
    """
    this function will return a database connection object
    if the connection object does not exist, it will create one
    if it exists, it will return the existing one
    """
    if 'db' not in g:  ## check if the connection object exists in the global object g
        g.db = mysql.connector.connect(  ## create a connection object and store it in the global object g
            host=current_app.config['DB_HOST'],  ## get the host from the config file
            port=current_app.config['DB_PORT'],  ## get the port from the config file
            user=current_app.config['DB_USER'],  ## get the user from the config file
            password=current_app.config['DB_PASSWORD'],  ## get the password from the config file
            database=current_app.config['DB_NAME']  ## get the database name from the config file
        )
        g.db.autocommit = True  ## set autocommit to true, so we don't have to commit after every query

    return g.db  ## return the connection object


def close_db(e=None):
    """
    this function will close the database connection
    if the connection object exists, it will close it
    """
    db = g.pop('db', None)  ## get the connection object from the global object g and remove it from g

    if db is not None:  ## check if the connection object exists
                db.close()  ## close the connection object 
        
def init_app(app):
    """
    this function will register the close_db function to be called when the app context ends
    """
    app.teardown_appcontext(close_db)  ## register the close_db function to be called when the app context ends

def query_test(sql, params=()):
    """
    this function will execute a sql query and return the result
    it will take two arguments:
    - sql: the sql query to be executed
    - params: the parameters to be passed to the sql query
    """
    conn = get_db()  ## get the connection object
    with conn.cursor(dictionary=True) as cursor:  ## create a cursor object
        cursor.execute(sql, params)  ## execute the sql query with the parameters
        row = cursor.fetchone()  ## fetch one row from the result
        return True if row else False  ## return True if the row exists, else return False