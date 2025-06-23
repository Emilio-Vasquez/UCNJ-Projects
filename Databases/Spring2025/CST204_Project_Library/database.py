import hashlib
from models import user
from app import create_app, db
from werkzeug.security import check_password_hash

app = create_app()

def list_users():
    # Query to get all user IDs
    with app.app_context():
        users = user.query.with_entities(user.username).all()
        return [u.username for u in users]
   
def verify(username, password):
    with app.app_context():
        user_instance = user.query.filter_by(username=username).first()  # Retrieve the user by ID

        if user_instance:
            print(f"Stored Password Hash: {user_instance.password}")  # Print stored hash (for debugging)
            print(f"Submitted password: {password}")
            if check_password_hash(user_instance.password, password):
                return True
            else:
                print("Password mismatch!")
        else:
            print("User not found")
        return False  # If no user found
        