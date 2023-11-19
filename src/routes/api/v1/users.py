from sqlalchemy.util.deprecations import os
from src.models.response import Response
from src.middlewares.jwt import jwt_required
from src.utils.validators import is_valid_json_user
from src.services.mail_service import send_create_account
from src.models.user import TUSER
from flask import Blueprint, jsonify, request
from src.database.db import db


usersRoutes = Blueprint("users", __name__, url_prefix="/users")


@usersRoutes.get("/")
@jwt_required("usuariros", ["listar usuarios"])
def list_users():
    users = TUSER.query.all()
    return Response.new("Lista de usuarios", data=[user.to_json() for user in users])


# @jwt_required("usuariros", ["crear usuarios"])
@usersRoutes.post("/")
def create_user():
    json_user = request.json

    new_user = TUSER().from_json(json_user)

    db.session.add(new_user)
    db.session.commit()

    if os.getenv("ENV") != "test" and not send_create_account(
        {
            "id": new_user.id,
            "name": f"{new_user.first_name} {new_user.first_surname}",
            "email": new_user.email,
        }
    ):
        return Response.fail("Error al mandar el correo de confirmación"), 400

    return Response.new("Usuario creado correctamente", data=new_user.to_json())


@usersRoutes.get("/<int:id>")
def get_user(id: int):
    user = TUSER.query.get(id)
    if user is None:
        return jsonify({"message": "Usuario no encontrado"}), 400

    return jsonify(user.to_json())


@usersRoutes.delete("/<int:id>")
def delete_user(id: int):
    if id == 1:
        return jsonify({"message": "Acceso denegado"})

    user = TUSER.query.get(id)
    if user is None:
        return jsonify({"message": "Usuario no encontrado"}), 400
    user.state = "inactive"
    db.session.commit()

    return jsonify(user.to_json())


@usersRoutes.put("/<int:id>")
def update_user(id: int):
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

    return Response.new("Usuario actualizado correctamente", data=user.to_json())


@usersRoutes.post("/send")
def send():
    if send_create_account({"name": "Andres", "email": "andrescopeticona7@gmail.com"}):
        return "correct", 200

    return "incorrect", 400
