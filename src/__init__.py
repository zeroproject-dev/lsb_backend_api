from flask_socketio import SocketIO
from .app import app

socketio = SocketIO(app)


@socketio.on("connect")
def connect(socket):
    print("user connected")
    print(socket)


@socketio.on("translate")
def translate(test):
    print("translate")
    print(len(test["data"]))
    return
