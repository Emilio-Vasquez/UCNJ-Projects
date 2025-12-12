from flask import request, flash, redirect, url_for ## Import: Imports necessary functions and objects from the Flask framework:
from .db import get_db

def handle_login(): ## Defines the function named handle_login(), which will be mapped to the /login route in your Flask application.
    if request.method == "POST":
        email = request.form.get('email') ## Form Data Retrieval: Retrieves the value of the input field with name="email" from the submitted form data
        password = request.form.get('password')

        #Validate login using SQL/Database
        db = get_db()
        cursor = db.cursor(dictionary=True)


        cursor.execute(
            'SELECT * FROM users WHERE email = %s AND password = %s', 
            (email, password) ## Provides the Python variables (email, password) to substitute for the placeholders
        )

        
        ## Executes the query and fetches the first (and hopefully only) matching row from the database, 
        ## assigning it to the user variable. If no match is found, user will be None.
        user = cursor.fetchone()
        
        if user:
            # if Login successful, it will redirect to home page
            print(f"Login successful: {email}")
            return redirect(url_for('main.home'))
        else:
            # Login failed
            print("Login failed: Invalid email or password")
            flash('Invalid email or password!', 'error')

    
    return None
