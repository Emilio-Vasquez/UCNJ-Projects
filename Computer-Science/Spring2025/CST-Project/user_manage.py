# user_management.py
from flask import request, jsonify, session
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
from db_connection import get_db_connection
from config import Config
import mysql.connector

bcrypt = Bcrypt()
mail = Mail()

def signup():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    if not username or not password or not email:
        return jsonify({"error": "Username, password, and email are required"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("INSERT INTO users (username, password_hash, email, cash, lives) VALUES (%s, %s, %s, 500, 0)", (username, hashed_password, email))
        db.commit()

        msg = Message('Welcome to Trivia Game!', recipients=[email])
        msg.body = f"Hi {username},\n\nThank you for signing up! You received $500 virtual currency to start playing.\n\nEnjoy!"
        mail.send(msg)

        return jsonify({"message": "Signup successful"}), 201
    except mysql.connector.IntegrityError:
        return jsonify({"error": "Username or email already taken"}), 400
    finally:
        cursor.close()
        db.close()

def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    cursor.close()
    db.close()

    if user and bcrypt.check_password_hash(user['password_hash'], password):
        session['user_id'] = user['user_id']
        return jsonify({
            "message": "Login successful",
            "user_id": user['user_id'],
            "cash": user['cash'],
            "lives": user['lives']
        }), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401