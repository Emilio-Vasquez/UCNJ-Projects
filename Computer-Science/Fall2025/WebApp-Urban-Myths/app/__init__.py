from flask import Flask
from config import Config
from .db import init_app
from .routes import main

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")

    # 🔥 THIS LINE IS REQUIRED
    app.config.from_object(Config)

    init_app(app)
    app.register_blueprint(main)

    return app