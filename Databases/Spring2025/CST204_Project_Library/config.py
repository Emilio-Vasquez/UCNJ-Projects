# Flask Config File
import os

class Config:
    # SECRET_KEY = os.urandom(24)  # Use a random secret key for sessions
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Use os.getenv to get values from environment variables
    # SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
    
    # Email configuration
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = os.getenv('MAIL_PORT')
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
