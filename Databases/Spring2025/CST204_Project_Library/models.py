from app import db
from sqlalchemy import Enum
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


# Define Models for your tables
class user(db.Model):
    __tablename__ = 'users'  # Specify your actual table name

    # Define your columns here
    user_id  = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    is_verified = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    def __init__(self, username, password, email, is_verified=False, is_admin=False):
        self.username = username
        self.password = password
        self.email = email
        self.is_verified = is_verified
        self.is_admin = is_admin

             
    def __repr__(self):
        return f'<User {self.user_id}, {self.username}>'
    
    def verify_password(self, password):
        return check_password_hash(self.password, password)

class admin_request(db.Model):
    __tablename__ ='admin_requests'

    # Define your columns here
    request_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    request_date = db.Column(db.DateTime, default=datetime.utcnow)  # Default to today if not provided
    status = db.Column(Enum('Pending', 'Approved', 'Denied', name='status_enum'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)  # Foreign key referencing User model

    def __init__(self, request_date=None, status=None, user_id=None):
        if request_date is not None:
            self.request_date = request_date
        if status is not None:
            self.status = status
        if user_id is not None:
            self.user_id = user_id

class Category(db.Model):
    __tablename__ = 'categories'

    # Define your columns here
    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(100), unique=True, nullable=False)

    def __init__(self, category_name):
        self.category_name = category_name

class Publisher(db.Model):
    __tablename__ = 'publishers'

    # Define your columns here
    publisher_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    publisher_name = db.Column(db.String(150), nullable=False)
    contact_info = db.Column(db.String(255))

    def __init__(self, publisher_name, contact_info=None):
        self.publisher_name = publisher_name
        self.contact_info = contact_info

class Book(db.Model):
    __tablename__ = 'books'

    # Define your columns here
    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(150), nullable=False)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'))
    publisher_id = db.Column(db.Integer, db.ForeignKey('publishers.publisher_id'))
    year_published = db.Column(db.Integer)  # Store year as integer
    copies_available = db.Column(db.Integer, default=0)

    def __init__(self, title, author, isbn, category_id=None, publisher_id=None, year_published=None, copies_available=0):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.category_id = category_id
        self.publisher_id = publisher_id
        self.year_published = year_published
        self.copies_available = copies_available

class Loan(db.Model):
    __tablename__ = 'loan'

    # Define your columns here
    loan_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'), nullable=False)
    loan_date = db.Column(db.Date, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date)
    is_overdue = db.Column(db.Boolean, default=False)
    fine_amount = db.Column(db.Numeric(6, 2), default=0.00)

    def __init__(self, user_id, book_id, loan_date, due_date, return_date=None, is_overdue=False, fine_amount=0.00):
        self.user_id = user_id
        self.book_id = book_id
        self.loan_date = loan_date
        self.due_date = due_date
        self.return_date = return_date
        self.is_overdue = is_overdue
        self.fine_amount = fine_amount

class Reservation(db.Model):
    __tablename__ = 'reservations'

    # Define your columns here
    reservation_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'), nullable=False)
    reservation_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.Enum('Pending', 'Completed', name='reservation_status_enum'), default='Pending', nullable=False)

    def __init__(self, user_id, book_id, reservation_date, status='Pending'):
        self.user_id = user_id
        self.book_id = book_id
        self.reservation_date = reservation_date
        self.status = status
