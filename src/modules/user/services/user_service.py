from flask import Request
from src.modules.user.models.user_schema import is_valid_json_user
from src.services.mail_service import send_create_account
from ..models.user import TUSER
from src.database.db import db
from src.modules.user.dto.user_filter import get_filters


def list_users(request: Request) -> list[dict]:
    users = get_filters(request).all()
    users = [user.to_json() for user in users]
    return users


def create_user(json: dict | None):
    if not is_valid_json_user(json):
        return None

    db.session.begin()

    new_user = TUSER().from_json(json)

    try:
        db.session.add(new_user)
    except Exception as e:
        print(e)
        db.session.rollback()
        return None

    if not send_create_account(new_user):
        print("Error to send email to: ", new_user["email"])

    db.session.flush()
    db.session.commit()

    return new_user.to_json()


def get_user_by_id(id: int):
    user: TUSER | None = TUSER.query.get(id)

    if user is None:
        return None

    return user.to_json()


def delete_user(id: int):
    if id == 1:
        return None

    user = TUSER.query.get(id)
    if user is None:
        return None

    user.state = "inactive"
    db.session.commit()

    return user.json_user()


def update_user(id: int, data: dict | None) -> dict | None:
    if id == 1:
        return None

    if not is_valid_json_user(data):
        return None

    user = TUSER.query.get(id)

    if user is None:
        return None

    user.from_json(data)
    db.session.commit()

    return user.to_json()
