from sqlalchemy.sql.operators import or_
from middlewares.jwt import jwt_required
import os
from models.response import Response
from services.mail_service import send_create_account
from models.user import TUSER
from flask import Blueprint, jsonify, request
from database.db import db

usersRoutes = Blueprint("users", __name__, url_prefix="/users")


@usersRoutes.get("/")
@jwt_required("usuarios", ["Listar usuarios"])
def list_users():
    search_param = request.args.get("search")

    if search_param:
        users = TUSER.query.filter(
            or_(
                TUSER.first_name.ilike(f"%{search_param}%"),
                TUSER.first_surname.ilike(f"%{search_param}%"),
            )
        ).all()
    else:
        users = TUSER.query.all()

    users = [user.to_json() for user in users]    

    return Response.new("Lista de usuarios", data=users)


@usersRoutes.post("/")
@jwt_required("usuarios", ["agregar usuario"])
def create_user():
    json_user = request.json

    new_user = TUSER().from_json(json_user)

    if os.getenv("ENV") == "test":
        new_user[
            "password"
        ] = "sha256$DqBixignPwmuuduT$77efdc09a8f62a3339ce905c5358334bd9a11f8313d256a6872f0ca91500515e"

    db.session.add(new_user)
    db.session.commit()

    if os.getenv("ENV") != "test" and not send_create_account(
        {
            "id": new_user.id,
            "name": f"{new_user.first_name} {new_user.first_surname}",
            "email": new_user.email,
        }
    ):
        print("error al mandar")
        db.session.rollback()
        return Response.fail("Error al mandar el correo de confirmación"), 400

    return Response.success("Usuario creado correctamente", data=new_user.to_json())


@usersRoutes.get("/<int:id>/")
@jwt_required("usuarios", ["Listar usuarios"])
def get_user(id: int):
    user = TUSER.query.get(id)
    if user is None:
        return Response.fail("Usuario no encontrado"), 400

    return Response.success("Usuario", user.to_json())


@usersRoutes.delete("/<int:id>/")
@jwt_required("usuarios", ["eliminar usuario"])
def delete_user(id: int):
    if id == 1:
        return jsonify({"message": "Acceso denegado"})

    user = TUSER.query.get(id)
    if user is None:
        return jsonify({"message": "Usuario no encontrado"}), 400

    user.state = "inactive"
    db.session.commit()

    return Response.success("Usuario desactivado correctamente", user.json_user())


@usersRoutes.put("/<int:id>/")
@jwt_required("usuarios", ["modificar usuario"])
def update_user(id: int):
    if id == 1:
        return Response.fail("Acceso denegado"), 400

    json_user = request.json
    # if not is_valid_json_user(json_user):
    #     return Response.fail("Petición incorrecta"), 400

    user = TUSER.query.get(id)
    if user is None:
        return Response.fail("Usuario no encontrado"), 400

    user.from_json(json_user)
    db.session.commit()

    return Response.new("Usuario actualizado correctamente", data=user.to_json())


@usersRoutes.post("/send")
def send():
    if send_create_account({"name": "Andres", "email": "andrescopeticona7@gmail.com", "id": 1}):
        return "correct", 200

    return "incorrect", 400
