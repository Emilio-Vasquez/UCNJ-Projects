from flask import request, flash, redirect, url_for
from .db import get_db

def handle_registration():
    if request.method == "POST":
    
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        print(f"Registration attempt: {name}, {email}")
        
        # Validate user registration, then use SQL to register user into database
        if password == confirm_password:
           
            db = get_db()
            cursor = db.cursor(dictionary=True) # checking if email already exist or not
            
            cursor.execute(
                'SELECT * FROM users WHERE email = %s', 
                (email,)
            )
            existing_user = cursor.fetchone()

            print("name,email,passowrd checkup")
            print(name, email, password)

            if existing_user:
                print(" Registration failed: Email already exists")
                flash('Email already registered!', 'error')
            else:
                # Save to database
                cursor.execute(
                    'INSERT INTO users (username, email, password) VALUES (%s, %s, %s)',
                    (name, email, password)
                )
                db.commit()
                
                print(f"Registration successful: {name}, {email}")
                flash('Registration successful! Please login.', 'success')
                return redirect(url_for('main.login'))
        else:
            print(" Passwords don't match")
            flash('Passwords do not match!', 'error')
    
    return None
