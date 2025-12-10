"""
This is the initialization file for the MypythonWebApp package.
it acts like the glue for the entire application
it essentially formats the app/ folder as a package
giving us the ability to basically ijmport scripts from this folder
It also loads the configurations from the config file, and it initializes extensions, as well as 
regestiring blueprints(routes) into the application
"""
from dotenv import load_dotenv
load_dotenv()
from flask import Flask ##this class FLask lets us create an instance of flask
from .db import init_app ## this is the function that closes our db connection automatically
from .routes import bp
import os ##well create this file later, with reports
## and well imprt blueprint here
## and we do that to register routes into our application

def create_app():
    """
    will be to have it run on our "run.py" to create the app and it running on a development server
    """


    app = Flask(__name__, template_folder="templates", static_folder ="static")
    ##the double underscore "name" is a built in variable to get the name of the current file
    #   ## create an instance of the flask class
    ## and were trying to regsiter the template folder and the static folder into our flask app
    import config
    app.config.from_object("config.config")
    init_app(app)  ## this will register the close_db function to be called when the app context ends

    app.register_blueprint(bp) ## this will register the blueprint into our application

    return app
    ## return the app instance
        