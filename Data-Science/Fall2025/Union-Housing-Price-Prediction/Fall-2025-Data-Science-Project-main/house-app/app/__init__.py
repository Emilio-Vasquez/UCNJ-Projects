from flask import Flask, render_template,request
from .db import init_app
from .routes import bp

def create_app():
    #Have it rUn on run.py, and leave it running in a development server

    app = Flask(__name__, template_folder='templates', static_folder='static')
    #__name__ gets name of current file,

    app.config.from_object('config.Config')

    init_app(app)

    app.register_blueprint(bp)

    return app

