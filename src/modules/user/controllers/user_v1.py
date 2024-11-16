from src.middlewares.jwt import jwt_required
from src.models.response import Response
from src.modules.user.services.user_service import (
    create_user,
    delete_user,
    get_user_by_id,
    list_users,
    update_user,
)
from flask import Blueprint, jsonify, request

usersV1Routes: Blueprint = Blueprint("users", __name__, url_prefix="/users")


@usersV1Routes.get("/")
@jwt_required("usuarios", ["Listar usuarios"])
def get_list_users():
    return Response.new("Lista de usuarios", data=list_users(request))


@usersV1Routes.post("/")
@jwt_required("usuarios", ["agregar usuario"])
def post_create_user():
    user = create_user(request.json)

    if user is None:
        return Response.fail("Error al crear el usuario"), 400

    return Response.success("Usuario creado correctamente", data=user)


@usersV1Routes.get("/<int:id>/")
@jwt_required("usuarios", ["Listar usuarios"])
def get_user(id: int):
    user = get_user_by_id(id)

    if user is None:
        return Response.fail("Usuario no encontrado"), 400

    return Response.success("Usuario", data=user)


@usersV1Routes.delete("/<int:id>/")
@jwt_required("usuarios", ["eliminar usuario"])
def delete_delete_user(id: int):
    if id == 1:
        return jsonify({"message": "Acceso denegado"})

    user_deleted = delete_user(id)

    if user_deleted is None:
        return jsonify({"message": "Error al eliminar el usuario"}), 400

    return Response.success("Usuario eliminó correctamente", data=user_deleted)


@usersV1Routes.put("/<int:id>/")
@jwt_required("usuarios", ["modificar usuario"])
def put_update_user(id: int):
    if id == 1:
        return Response.fail("Acceso denegado"), 400

    user = update_user(id, request.json)

    if user is None:
        return Response.fail("Error al actualizar el usuario"), 400

    return Response.new("Usuario actualizado correctamente", data=user)
