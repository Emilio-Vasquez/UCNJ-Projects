from flask import Flask, request, jsonify, session, render_template, redirect, url_for
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_mail import Mail, Message
import pymysql
from dotenv import load_dotenv
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import pickle
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask_session import Session
import datetime
import base64
import os

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'  ## this lets the OAuth (which requires https or security) use our http

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default_key')

bcrypt = Bcrypt(app)
CORS(app)

CLIENTS_SECRETS_FILE = "client_secret.json" ## json file with client id
SCOPES = ['https://www.googleapis.com/auth/gmail.send']
REDIRECT_URI = "http://localhost:5000/callback"

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'pycodequiz@gmail.com'
app.config['MAIL_PASSWORD'] = 'dhydjvenutwwacwn'
app.config['MAIL_DEFAULT_SENDER'] = 'pycodequiz@gmail.com'

mail = Mail(app)

def get_db_connection():
    return pymysql.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/authorize')
def authorize():
    flow = Flow.from_client_secrets_file(
        CLIENTS_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )
    authorization_url, state = flow.authorization_url(prompt='consent')
    session['state'] = state
    return redirect(authorization_url)

@app.route('/callback')
def callback():
    flow = Flow.from_client_secrets_file(
        CLIENTS_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )
    flow.fetch_token(authorization_response=request.url)
    credentials = flow.credentials

    session['credentials'] = pickle.dumps(credentials)

    with open('gmail_token.pkl', 'wb') as token:
        pickle.dump(credentials, token)

    # Update user's Gmail authentication status
    if 'user_id' in session:
        db = get_db_connection()
        with db.cursor() as cursor:
            cursor.execute("""
                UPDATE users 
                SET gmail_authenticated = 1 
                WHERE user_id = %s""", 
                (session['user_id'],))
            db.commit()
            
            # Get updated user data
            cursor.execute("SELECT * FROM users WHERE user_id = %s", (session['user_id'],))
            user = cursor.fetchone()
        db.close()

        # Send welcome email if needed
        if 'user_email' in session:
            send_welcome_email(session['user_email'])
        
        print(f"Gmail authentication completed for user {session['user_id']}")
        # Redirect to home page instead of login page
        return redirect(url_for('home'))
    else:
        print("No user_id in session during callback")
        # If somehow there's no session, redirect to login
        return redirect(url_for('login_page'))


def load_gmail_credentials():
    try:
        with open('gmail_token.pkl', 'rb') as token:
            credentials = pickle.load(token)
        if credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
            with open('gmail_token.pkl', 'wb') as token:
                pickle.dump(credentials, token)
        return credentials
    except Exception as e:
        print("Failed to load Gmail credentials:", e)
        return None

def send_welcome_email(recipient_email):
    credentials = load_gmail_credentials()
    if not credentials:
        print("Credentials not available.")
        return

    service = build('gmail', 'v1', credentials=credentials)
    message = MIMEMultipart()
    message['to'] = recipient_email
    message['from'] = 'pycodequiz@gmail.com'  # Add this line
    message['subject'] = 'Welcome to Pycode!'
    body = 'Hello, \n\nThank you for signing up to Pycode. Have fun and good luck!'
    message.attach(MIMEText(body, 'plain'))

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    try:
        service.users().messages().send(userId='pycodequiz@gmail.com', body={'raw': raw_message}).execute()
        print("Welcome email sent!")
    except Exception as error:
        print(f"Error sending email: {error}")

@app.route('/signup', methods=['POST'])
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
        with db.cursor() as cursor:
            cursor.execute(""" 
                INSERT INTO users 
                (username, password_hash, email, cash, lives, gmail_authenticated) 
                VALUES (%s, %s, %s, 500, 0, 0)""",
                (username, hashed_password, email))
            db.commit()
            
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            
            # Set session variables to maintain login state
            session['user_email'] = email
            session['user_id'] = user['user_id']
            print(f"User signup successful, user_id {user['user_id']} added to session")

        # Return URL for Gmail authorization
        return jsonify({
            "message": "Signup successful!", 
            "user_id": user['user_id'],
            "redirect": url_for('authorize')
        }), 200

    except pymysql.err.IntegrityError:
        return jsonify({"error": "Username or email already taken"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@app.route('/')
def home():
    if 'user_id' not in session:
        # Debug print to help understand the issue
        print("No user_id in session, redirecting to login page")
        return redirect(url_for('login_page'))
    
    # Debug print to confirm session exists
    print(f"User {session['user_id']} is in session, displaying main page")
    return render_template('main_pg.html')

@app.route('/signup_page')
def signup_page():
    if 'user_id' in session:
        return redirect(url_for('home'))
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_page'))

@app.route('/level1')
def level1_page():
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    return render_template('LVL-1.html')

@app.route('/level2')
def level2_page():
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    return render_template('LVL-2.html')

@app.route('/level3')
def level3_page():
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    return render_template('LVL-3.html')

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    # If user is already logged in, redirect to home
    if 'user_id' in session:
        print(f"User already logged in with ID: {session['user_id']}, redirecting to home")
        return redirect(url_for('home')) if request.method == 'GET' else jsonify({"redirect": url_for('home')}), 200
        
    if request.method == 'POST':
        data = request.json
        username = data.get('username')
        password = data.get('password')

        db = get_db_connection()
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
        db.close()

        if user and bcrypt.check_password_hash(user['password_hash'], password):
            # Add debug print when setting session
            print(f"Login successful for user: {username}, setting session")
            session['user_id'] = user['user_id']
            session['user_email'] = user['email']
            
            # Check if user needs Gmail authentication
            if not user.get('gmail_authenticated'):
                print(f"User {user['user_id']} needs Gmail authentication, redirecting")
                return jsonify({
                    "message": "Login successful",
                    "needs_gmail_auth": True,
                    "redirect": url_for('authorize')
                }), 200
            
            # User is fully authenticated
            print(f"User {user['user_id']} is fully authenticated")
            return jsonify({
                "message": "Login successful",
                "user_id": user['user_id'],
                "cash": user['cash'],
                "lives": user['lives'],
                "redirect": url_for('home')
            }), 200
        else:
            return jsonify({"error": "Invalid username or password"}), 401

    # Add debug print for GET request to login page
    print("Displaying login page")
    return render_template('login.html')

@app.route('/get_balance', methods=['GET'])
def get_balance():
    user_id = session.get('user_id')
    if user_id:
        db = get_db_connection()
        with db.cursor() as cursor:
            cursor.execute("SELECT cash, lives FROM users WHERE user_id = %s", (user_id,))
            balance = cursor.fetchone()
        db.close()
        return jsonify({'cash': balance['cash'], 'lives': balance['lives']})
    else:
        return jsonify({'error': 'User not logged in'}), 400

@app.route('/purchase_life', methods=['POST'])
def purchase_life():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "User not logged in"}), 400

    db = get_db_connection()
    try:
        with db.cursor() as cursor:
            cursor.execute("SELECT cash, lives, email FROM users WHERE user_id = %s", (user_id,))
            user = cursor.fetchone()

            if not user:
                return jsonify({"error": "User not found"}), 404

            if user['cash'] >= 100:
                new_cash = user['cash'] - 100
                new_lives = user['lives'] + 1
                cursor.execute("UPDATE users SET cash = %s, lives = %s WHERE user_id = %s", (new_cash, new_lives, user_id))
                db.commit()

                # Updated email sending
                msg = Message(
                    'Life Purchased',
                    sender='pycodequiz@gmail.com',
                    recipients=[user['email']]
                )
                msg.body = "You successfully purchased a life for $100. Good luck on your next quiz!"
                mail.send(msg)

                return jsonify({"message": "Life purchased successfully", "cash": new_cash, "lives": new_lives}), 200
            else:
                return jsonify({"error": "Not enough cash to purchase a life"}), 400
    except Exception as err:
        return jsonify({"error": str(err)}), 500
    finally:
        db.close()


@app.route('/earn_cash', methods=['POST'])
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
        with db.cursor() as cursor:
            cursor.execute("UPDATE users SET cash = cash + %s WHERE user_id = %s", (reward, user_id))
            cursor.execute("INSERT INTO transactions (user_id, type, amount) VALUES (%s, %s, %s)", (user_id, 'quiz_reward', reward))
            
            # Get user email
            cursor.execute("SELECT email FROM users WHERE user_id = %s", (user_id,))
            user_email = cursor.fetchone()['email']
        db.commit()
        db.close()

        # Send email notification for earning cash
        if reward > 0:
            msg = Message(
                'Cash Earned!',
                sender='pycodequiz@gmail.com',
                recipients=[user_email]
            )
            msg.body = f"Congratulations! You earned {reward} cash for completing the quiz!"
            mail.send(msg)

        return jsonify({'message': f'You earned {reward} cash!'})

    return jsonify({'error': 'User not logged in'}), 400

@app.route('/take_quiz', methods=['POST'])
def take_quiz():
    user_id = session.get('user_id')
    if user_id:
        db = get_db_connection()
        with db.cursor() as cursor:
            cursor.execute("SELECT lives FROM users WHERE user_id = %s", (user_id,))
            lives = cursor.fetchone()['lives']

            if lives > 0:
                cursor.execute("UPDATE users SET lives = lives - 1 WHERE user_id = %s", (user_id,))
                db.commit()
                db.close()
                return jsonify({'message': 'Quiz started!'})
            else:
                db.close()
                return jsonify({'error': 'Not enough lives'}), 400
    else:
        return jsonify({'error': 'User not logged in'}), 400

@app.route('/forgot_password', methods=['POST'])
def forgot_password():
    data = request.json
    email = data.get('email')

    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.execute("SELECT username FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
    db.close()

    if user:
        msg = Message('Password Reset Request', recipients=[email])
        msg.body = (
            f"Hi {user['username']},\n\nIf you forgot your password, please contact support or visit your profile to change it securely.\n\nThis is an automated message."
        )
        mail.send(msg)
        return jsonify({'message': 'Password reset email sent.'}), 200
    else:
        return jsonify({'error': 'Email not found'}), 404

@app.route('/check_username', methods=['POST'])
def check_username():
    data = request.json
    username = data.get('username')

    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
    db.close()

    return jsonify({"available": not bool(user)})

@app.route('/routes')
def list_routes():
    import urllib
    output = []
    for rule in app.url_map.iter_rules():
        methods = ','.join(rule.methods)
        line = urllib.parse.unquote(f"{rule.endpoint:30s} {methods:20s} {rule}")
        output.append(line)
    return '<pre>' + '\n'.join(sorted(output)) + '</pre>'

@app.route('/debug_session')
def debug_session():
    session_content = {key: session[key] for key in session}
    return jsonify({
        "session_contains": session_content,
        "user_id_exists": 'user_id' in session
    })

if __name__ == '__main__':
    app.run(debug=True)