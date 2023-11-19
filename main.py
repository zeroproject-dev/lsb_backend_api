import os

from src import app
from src import socketio

# from database.db import db
#
# with app.app_context():
#     db.create_all()


if __name__ == "__main__":
    socketio.run(
        app,
        use_reloader=True,
        log_output=True,
        port=3300,
        debug=os.getenv("ENV") == "debug" or os.getenv("ENV") == "test",
        host="0.0.0.0",
    )
