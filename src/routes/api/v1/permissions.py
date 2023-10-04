from flask import Blueprint, jsonify, request
from database.db import db
from middlewares.users_check import check_users_list, \
    check_users_modify
from models.role import TPERMISSION
from utils.roles import get_all_modules_permissions

from utils.validators import is_valid_json_role

permissionRoute = Blueprint("permissions", __name__, url_prefix="/permissions")


@permissionRoute.get("/")
def list_all():
    # is_authorized, msg = check_users_list()
    # if not is_authorized:
    #     return jsonify({"message": msg}), 400

    perms = get_all_modules_permissions()
    return jsonify(perms)


@permissionRoute.get("/<int:id>")
def get_by_id(id: int):
    is_authorized, msg = check_users_list()
    if not is_authorized:
        return jsonify({"message": msg}), 400

    obj = TPERMISSION.query.get(id)
    if obj is None:
        return jsonify({"message": "Permiso no encontrado"}), 400

    response = obj.to_json()

    return jsonify(response)


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
