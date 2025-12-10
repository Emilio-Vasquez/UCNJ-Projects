from flask import redirect
import hashlib
from .db import get_db   # connects to mysql

USERNAME_MIN_LENGTH = 5 # user must be 5 characters min
USERNAME_MAX_LENGTH = 30
PASSWORD_MIN_LENGTH = 8 # pw must be 8 characters min
PASSWORD_SYMBOLS = "!@#$%^&*()_+-=[]{}|;:',.<>?/"

def validate_password(password):
    # makes sure password meets all requirements
    # Returns True if valid, False if not.
    if len(password) < PASSWORD_MIN_LENGTH:
        return False # if the password is too short it's invalid
    
    has_uppercase = any(char.isupper() for char in password)
    has_lowercase = any(char.islower() for char in password)
    has_symbol = any(char in PASSWORD_SYMBOLS for char in password)
    
    return has_uppercase and has_lowercase and has_symbol
    # if all conditions are met, it returns true

def handle_registration(request): #Handles user registration and stores user details in MySQL.
    # gets form data / request.form works as a dictionary
    email = request.form.get("email")
    username = request.form.get("username")
    password = request.form.get("password")
    
    if len(username) < USERNAME_MIN_LENGTH or len(username) > USERNAME_MAX_LENGTH: # ^^^ if username isn't valid
        return redirect("/registration?error=username") # query parameter w/ name + value, passes a message on
    
    if not validate_password(password): # if the password wasn't valid
        return redirect("/registration?error=password") ##
    
    # hashing the password before its stored
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    # connects to DB
    db = get_db()
    cursor = db.cursor()

    # inserts inputted info into users table in sql
    sql = """
        INSERT INTO users (email, username, password)
        VALUES (%s, %s, %s)
    """
    cursor.execute(sql, (email, username, hashed_password)) # fills polaceholders (%s)
    db.commit() # makes sure the data is stored
    cursor.close()

    # after successful registration, go to login page
    return redirect("/login")
