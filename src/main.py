import os

from app import app

# from database.db import db
#
# with app.app_context():
#     db.create_all()


if __name__ == "__main__":
    app.run(
        port=3300,
        debug=os.getenv("ENV") == "debug" or os.getenv("ENV") == "test",
        host="0.0.0.0",
    )
