from flask import Blueprint, jsonify, request
from database.db import db
from middlewares.users_check import check_users_delete, check_users_list, check_users_modify, check_users_register

from models.user import TUSER
from services.mail_service import send_create_account, send_mail
from utils.validators import is_valid_json_user

usersRoutes = Blueprint("users", __name__, url_prefix="/users")


@usersRoutes.get("/")
def list_users():
    user, msg = check_users_list()
    if user is None:
        return jsonify({"message": msg}), 400

    users = TUSER.query.all()
    return jsonify([user.to_json() for user in users])


@usersRoutes.post("/")
def create_user():
    user, msg = check_users_register()
    if user is None:
        return jsonify({"message": msg}), 400

    json_user = request.json
    if not is_valid_json_user(json_user):
        return jsonify({"message": "Petición incorrecta"}), 400

    new_user = TUSER().from_json(json_user)
    new_user.password = 'scrypt:32768:8:1$uVaQHFb8cbRFwQzH$6b02a47ca29fe9f57e4cc6669de83b9e4fffd76165d1bf85f8264635a6048a67990c85d4ee8bd7674647b5a05f7b7f40fa478bccd4382b710cd71e796b2b1369'
    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.to_json())


@usersRoutes.get("/<int:id>")
def get_user(id: int):
    user, msg = check_users_list()
    if user is None:
        return jsonify({"message": msg}), 400

    user = TUSER.query.get(id)
    if user is None:
        return jsonify({"message": "Usuario no encontrado"}), 400

    return jsonify(user.to_json())


@usersRoutes.delete("/<int:id>")
def delete_user(id: int):
    user, msg = check_users_delete()
    if user is None:
        return jsonify({"message": msg}), 400

    if id == 1:
        return jsonify({"message": "Acceso denegado"})

    user = TUSER.query.get(id)
    if user is None:
        return jsonify({"message": "Usuario no encontrado"}), 400
    user.state = 'inactive'
    db.session.commit()

    return jsonify(user.to_json())


@usersRoutes.put("/<int:id>")
def update_user(id: int):
    user, msg = check_users_modify()
    if user is None:
        return jsonify({"message": msg}), 400

    if id == 1:
        return jsonify({"message": "Acceso denegado"})

    json_user = request.json
    if not is_valid_json_user(json_user):
        return jsonify({"message": "Petición incorrecta"}), 400

    user = TUSER.query.get(id)
    if user is None:
        return jsonify({"message": "Usuario no encontrado"}), 400

    user.from_json(json_user)
    db.session.commit()

    return jsonify(user.to_json())


@usersRoutes.post("/send")
def send():
    if send_create_account(
            {'name': 'Andres', 'email': 'andrescopeticona7@gmail.com'}):
        return 'correct', 200

    return 'incorrect', 400
