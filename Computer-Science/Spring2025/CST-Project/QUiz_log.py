# quiz_logic.py
from flask import request, jsonify, session
from db_connection import get_db_connection

def take_quiz():
    user_id = session.get('user_id')
    if user_id:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT lives FROM users WHERE user_id = %s", (user_id,))
        lives = cursor.fetchone()['lives']

        if lives > 0:
            cursor.execute("UPDATE users SET lives = lives - 1 WHERE user_id = %s", (user_id,))
            db.commit()
            cursor.close()
            db.close()
            return jsonify({'message': 'Quiz started!'})
        else:
            cursor.close()
            db.close()
            return jsonify({'error': 'Not enough lives'}), 400
    else:
        return jsonify({'error': 'User not logged in'}), 400

def earn_cash():
    user_id = session.get('user_id')
    if user_id:
        score = request.json.get('score')
        level = request.json.get('level')
        reward = 0

        if level == 1:
            reward = 50 if score == 10 else 25 if score >= 6 else 0
        elif level == 2:
            reward = 100 if score == 10 else 50 if score >= 6 else 0
        elif level == 3:
            reward = 150 if score == 10 else 75 if score >= 6 else 0

        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("UPDATE users SET cash = cash + %s WHERE user_id = %s", (reward, user_id))
        db.commit()
        cursor.execute("INSERT INTO transactions (user_id, type, amount) VALUES (%s, %s, %s)", (user_id, 'quiz_reward', reward))
        db.commit()
        cursor.close()
        db.close()

        return jsonify({'message': f'You earned {reward} cash!'})

    return jsonify({'error': 'User not logged in'}), 400