import os 
from pathlib import Path 
from dotenv import load_dotenv

load_dotenv()

class Config:
    ## Get the project base directory 
    BASE_DIR = Path(__file__).resolve().parent

    SECRET_KEY = os.getenv("SECRET_KEY")

    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = int(os.getenv("DB_PORT"))
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_USER = os.getenv("DB_USER")
    DB_NAME = os.getenv("DB_NAME")

