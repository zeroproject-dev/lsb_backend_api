from flask import Blueprint, jsonify, request
from database.db import db
from middlewares.users_check import (
    check_users_delete,
    check_users_list,
)
from models.response import Response
from models.role import TROLE, TROLEPERMISSION
from utils.roles import get_id_permissions_of_module, get_permissions_of_role

from utils.validators import is_valid_json_role

roleRoutes = Blueprint("roles", __name__, url_prefix="/roles")


@roleRoutes.get("/")
def list_all():
    roles = TROLE.query.all()
    return jsonify([role.to_json() for role in roles])


@roleRoutes.post("/")
def create():
    # is_authorized, msg = check_users_register()
    # if not is_authorized:
    #     return jsonify({"message": msg}), 400

    # json = request.json
    # if not is_valid_json_role(json):
    #     return jsonify({"message": "Petición incorrecta"}), 400

    # new = TROLE().from_json(json)
    # db.session.add(new)
    # db.session.commit()

    json = request.json
    if json is None:
        return

    new = TROLE().from_json(json)
    db.session.add(new)
    db.session.commit()

    print(new.to_json())
    del json["name"]
    del json["description"]
    del json["state"]
    print(json)

    for key, value in json.items():
        permissions_ids = get_id_permissions_of_module(key)
        for i, v in enumerate(value):
            if v:
                new_perm = TROLEPERMISSION(new.id, permissions_ids[i])
                db.session.add(new_perm)

    db.session.commit()

    role_json = new.to_json()
    role_json["permissions"] = get_permissions_of_role(new.id)

    return Response.success("Rol creado correctamente", role_json)


@roleRoutes.get("/<int:id>")
def get_by_id(id: int):
    obj = TROLE.query.get(id)
    if obj is None:
        return jsonify({"message": "Rol no encontrado"}), 400

    response = obj.to_json()
    response["permissions"] = get_permissions_of_role(obj.id)

    return jsonify(response)


@roleRoutes.delete("/<int:id>")
def delete(id: int):
    if id == 1:
        return jsonify({"message": "Acceso denegado"})

    obj = TROLE.query.get(id)
    if obj is None:
        return jsonify({"message": "Rol no encontrado"}), 400
    obj.state = "inactive"
    db.session.commit()

    return jsonify(obj.to_json())


@roleRoutes.put("/<int:id>")
def update(id: int):
    if id == 1:
        return jsonify({"message": "Acceso denegado"})

    json = request.json
    if not is_valid_json_role(json):
        return jsonify({"message": "Petición incorrecta"}), 400

    obj = TROLE.query.get(id)
    if obj is None:
        return jsonify({"message": "Rol no encontrado"}), 400

    obj.from_json(json)
    db.session.commit()

    return jsonify(obj.to_json())
