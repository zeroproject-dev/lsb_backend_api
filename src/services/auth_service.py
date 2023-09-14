import pytz
import os
from datetime import datetime, timedelta
import jwt


class AuthService():

    jwt_key = os.getenv('JWT_KEY')
    tz = pytz.timezone("America/La_Paz")

    @classmethod
    def generate_token(cls, user):
        date_now = datetime.now(tz=cls.tz)
        payload = {
            'iat': date_now,
            'exp': date_now + timedelta(hours=10),
            'user': user.id,
        }

        return jwt.encode(payload, cls.jwt_key, algorithm="HS256")
