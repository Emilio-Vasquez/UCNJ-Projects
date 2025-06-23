# life_currency.py
from flask import request, jsonify, session  # <-- Import session here
from flask_mail import Message, Mail
import mysql.connector  # <-- Import mysql.connector here
from db_connection import get_db_connection
from config import Config

mail = Mail()

def get_balance():
    user_id = session.get('user_id')  # <-- session is now defined
    if user_id:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT cash, lives FROM users WHERE user_id = %s", (user_id,))
        balance = cursor.fetchone()
        cursor.close()
        db.close()
        return jsonify({'cash': balance['cash'], 'lives': balance['lives']})
    else:
        return jsonify({'error': 'User not logged in'}), 400

def purchase_life():
    user_id = request.json.get('user_id')

    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT cash, lives, email FROM users WHERE user_id = %s", (user_id,))
        user = cursor.fetchone()

        if not user:
            return jsonify({"error": "User not found"}), 404

        if user['cash'] >= 100:
            new_cash = user['cash'] - 100
            new_lives = user['lives'] + 1
            cursor.execute("UPDATE users SET cash = %s, lives = %s WHERE user_id = %s", (new_cash, new_lives, user_id))
            db.commit()

            msg = Message('Life Purchased', recipients=[user['email']])
            msg.body = "You successfully purchased a life for $100. Good luck on your next quiz!"
            mail.send(msg)

            return jsonify({"message": "Life purchased successfully"}), 200
        else:
            return jsonify({"error": "Not enough cash to purchase a life"}), 400
    except mysql.connector.Error as err:  # <-- Now mysql is defined
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        db.close()
