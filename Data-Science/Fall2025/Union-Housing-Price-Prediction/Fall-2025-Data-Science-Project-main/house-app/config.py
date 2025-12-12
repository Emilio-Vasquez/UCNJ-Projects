"""
This is the config.py script

This script will call the load_dotenv() function in order to extract our env variables

Then we will set up our application with these env variables

The keys we will call:
- Flask's secret key: SECRET_KEY
- Database's connection values:
    - DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME
"""

import os # We need to extract environment secret variables
from pathlib import Path #This is to extract the directory's path
from dotenv import load_dotenv #This is to pull the secret keys from the .env file

#First thing we do is, is load the variables from the .env file into the process environment (OS system)
load_dotenv()

class Config:
    """
    This is the configuration object
    """

    # Get the project base directorry
    BASE_DIR = Path(__file__).resolve().parent

    # Extract the Flask secret key::
    SECRET_KEY = os.getenv("SECRET_KEY")

    # Extract the MySQL Settings
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = int(os.getenv("DB_PORT"))
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")

