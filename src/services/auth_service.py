import pytz
import os
from datetime import datetime, timedelta
import jwt


class AuthService:
    jwt_key = os.getenv("JWT_KEY")
    tz = pytz.timezone("America/La_Paz")

    @classmethod
    def generate_token(cls, user):
        date_now = datetime.now(tz=cls.tz)
        payload = {
            "iat": date_now,
            "exp": date_now + timedelta(days=1),
            "user": user.id,
        }

        return jwt.encode(payload, cls.jwt_key, algorithm="HS256")

    @classmethod
    def generate_token_change_pw(cls, id):
        date_now = datetime.now(tz=cls.tz)
        payload = {
            "iat": date_now,
            "exp": date_now + timedelta(hours=1),
            "id": id,
        }

        return jwt.encode(payload, cls.jwt_key, algorithm="HS256")

    @classmethod
    def verify_token(cls, token):
        try:
            jwt.decode(token, os.getenv("JWT_KEY"), algorithms=["HS256"])
            return True
        except Exception:
            return False
