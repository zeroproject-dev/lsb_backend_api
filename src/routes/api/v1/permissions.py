from src.models.response import Response
from flask import Blueprint, jsonify, request
from src.database.db import db
from src.middlewares.users_check import check_users_modify
from src.models.role import TPERMISSION
from src.utils.roles import get_all_modules_permissions

from src.utils.validators import is_valid_json_role

permissionRoute = Blueprint("permissions", __name__, url_prefix="/permissions")


@permissionRoute.get("/")
def list_all():
    # is_authorized, msg = check_users_list()
    # if not is_authorized:
    #     return jsonify({"message": msg}), 400

    perms = get_all_modules_permissions()
    return Response.new("Lista de permisos", data=perms)


@permissionRoute.get("/<int:id>")
def get_by_id(id: int):
    # is_authorized, msg = check_users_list()
    # if not is_authorized:
    #     return jsonify({"message": msg}), 400

    obj = TPERMISSION.query.get(id)
    if obj is None:
        return jsonify({"message": "Permiso no encontrado"}), 400

    response = obj.to_json()

    return Response.new("Permiso", data=response)


@permissionRoute.put("/<int:id>")
def update(id: int):
    is_authorized, msg = check_users_modify()
    if not is_authorized:
        return jsonify({"message": msg}), 400

    json = request.json
    if not is_valid_json_role(json):
        return jsonify({"message": "Petición incorrecta"}), 400

    obj = TPERMISSION.query.get(id)
    if obj is None:
        return jsonify({"message": "Rol no encontrado"}), 400

    obj.from_json(json)
    db.session.commit()

    return jsonify(obj.to_json())
