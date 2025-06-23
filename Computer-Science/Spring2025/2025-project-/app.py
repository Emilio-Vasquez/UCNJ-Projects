from flask import Flask, render_template,request, redirect, url_for, flash
from hashlib import *;
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import bcrypt
import random
import string
import sqlite3

## 
app = Flask(__name__)

app.config['SECRET_KEY'] = 'secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # or use any database you prefer
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your_email_password'

db = SQLAlchemy(app)
mail = Mail(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    member_id = db.Column(db.String(120), unique=True, nullable=False)

# @app.route('/')
# def index():
#     return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']

    # Check if username and email are unique
    existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
    if existing_user:
        flash("Username or email already taken.")
        return redirect(url_for('index'))

    # Password hashing
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Generate a random member ID
    member_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

    # Create a new user object
    new_user = User(username=username, password=hashed_password, email=email, member_id=member_id)

    # Save user to the database
    db.session.add(new_user)
    db.session.commit()

    # Send verification email
    verification_link = f'http://127.0.0.1:5000/verify/{new_user.id}'
    send_verification_email(email, verification_link)

    flash("Registration successful! Please check your email to verify your account.")
    return redirect(url_for('index'))

def send_verification_email(email, verification_link):
    msg = Message("Verify Your Email", sender="your_email@gmail.com", recipients=[email])
    msg.body = f"Click the link to verify your email: {verification_link}"
    mail.send(msg)

@app.route('/verify/<int:user_id>')
def verify_email(user_id):
    user = User.query.get(user_id)
    if user:
        user.is_verified = True
        db.session.commit()
        flash("Your email has been verified! You can now log in.")
        return redirect(url_for('index'))
    else:
        flash("Invalid verification link.")
        return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username).first()
    if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        if user.is_verified:
            flash("Login successful!")
            return redirect(url_for('dashboard'))
        else:
            flash("Please verify your email before logging in.")
            return redirect(url_for('index'))
    else:
        flash("Invalid username or password.")
        return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    return "Welcome to your dashboard!"

if __name__ == '__main__':
    db.create_all()  # Creates the database tables if they don't exist
    app.run(debug=True)





## the instances that Flask creates, are used to 
## manage the outes (URL triggers)

#app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/dominican')
def dominican_recipe():
    return render_template('DominicanRecipe.html')

@app.route('/ecuadorian')
def ecuadorian_recipe():
    return render_template('EcuadorianRecipe.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/Login')
def Login():
    return render_template('Login.html')

@app.route('/shop')
def shop():
    return render_template('shop.html')


#login information tab##
#app = Flask(__name__)

# # Function to initialize DB
# def init_db():
#     conn = sqlite3.connect('users.db')
#     cursor = conn.cursor()
#     cursor.execute('''
#     CREATE TABLE IF NOT EXISTS users (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         username TEXT NOT NULL UNIQUE,
#         password TEXT NOT NULL
#     )
#     ''')
#     # Add a test user
#     cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ('testuser', 'testpass'))
#     conn.commit()
#     conn.close()

# init_db()

# # Route to display login form and process login
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']

#         conn = sqlite3.connect('users.db')
#         cursor = conn.cursor()

#         cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
#         user = cursor.fetchone()

#         conn.close()

#         if user:
#             return "Login successful! Welcome, " + username
#         else:
#             return "Invalid username or password."

#     return render_template('login.html')

if __name__ == '__main__':
    app 