"""
config.py script
this will call the load_dotenv() function in ordr to extract out env variables
then we will set up our application with these env variables
the keys we will call:
- flask's secret key: SECRET_KEY
-database's connection values:
    - DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME
"""

import os ##we need to extract enviorment secrect variables
from pathlib import Path ## this is to extract the direcrtorys path
from dotenv import load_dotenv  ## to pull the ssecret keys from the .env files

## first we do is, load the variables from the .env file into the process enviorment (os system)
load_dotenv()

class config:
    """
    this is the configuration object
    """

    ## get the nase directory
    BASE_DIR = Path(__file__).resolve().parent 
    ## C:/Users/deadbraincellss/templates/MypythonWebApp/config.py.  parent gets rid of config.py base directtory.

    ## Extract the flask's secret key
    SECRET_KEY = os.getenv("SECRET_KEY")

    ## extract the mysql settings:
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = int(os.getenv("DB_PORT", 3306))
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")
    print("DB_USER =", DB_USER)
    print("DB_PASSWORD =", DB_PASSWORD)
    print("DB_NAME =", DB_NAME)

