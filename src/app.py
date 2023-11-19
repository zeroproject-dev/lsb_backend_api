import os
from flask_cors import CORS
from flask import Flask, jsonify
from .database.db import db
from .routes.api import api
from dotenv import load_dotenv
from flask_socketio import SocketIO

load_dotenv()

BASE_PATH = os.getcwd()
STATIC = os.path.join(BASE_PATH, "static")
app = Flask(__name__, static_folder=STATIC)

CORS(app, resources={r"/api/*": {"origins": "*"}})

app.config["SECRET_KEY"] = (
    str(os.getenv("SECRET_KEY")) if os.getenv("SECRET_KEY") is not None else "test"
)

# Configure database
port = str(os.getenv("DB_PORT")) if os.getenv("DB_PORT") is not None else 3306
db_config = {
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "database": os.getenv("DB_NAME"),
    "port": int(port),
}

db_user = f"{db_config['user']}:{db_config['password']}"
db_host = f"{db_config['host']}:{db_config['port']}"

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"mysql://{db_user}@{db_host}/{db_config['database']}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

db.init_app(app)

app.register_blueprint(api)


@app.route("/")
def home():
    return jsonify({"message": "k ve"})
