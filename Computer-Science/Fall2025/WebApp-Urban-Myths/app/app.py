from flask import Flask
from app.routes import main   # import the blueprint cleanly

app = Flask(__name__)
app.register_blueprint(main)

if __name__ == "__main__":
    app.run(debug=True)
