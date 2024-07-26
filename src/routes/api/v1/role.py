from operator import or_
from flask import Blueprint, jsonify, request
from database.db import db
from models.response import Response
from models.role import TROLE, TROLEPERMISSION
from utils.roles import get_id_permissions_of_module, get_permissions_of_role

roleRoutes = Blueprint("roles", __name__, url_prefix="/roles")


@roleRoutes.get("/")
def list_all():
    search_param = request.args.get("search")

    if search_param:
        roles = TROLE.query.filter(
            or_(
                TROLE.name.ilike(f"%{search_param}%"),
                TROLE.description.ilike(f"%{search_param}%"),
            )
        ).all()
    else:
        roles = TROLE.query.all()

    res = []
    for role in roles:
        role = role.to_json()
        role["permissions"] = get_permissions_of_role(role["id"])
        res.append(role)

    return Response.success("Lista de roles", res)


@roleRoutes.post("/")
def create():
    # json = request.json
    # if not is_valid_json_role(json):
    #     return jsonify({"message": "Petición incorrecta"}), 400

    json = request.json
    if json is None:
        return

    new = TROLE().from_json(json)
    db.session.add(new)
    db.session.commit()

    del json["name"]
    del json["description"]
    del json["state"]

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


@roleRoutes.get("/<int:id>/")
def get_by_id(id: int):
    obj = TROLE.query.get(id)
    if obj is None:
        return jsonify({"message": "Rol no encontrado"}), 400

    response = obj.to_json()
    response["permissions"] = get_permissions_of_role(obj.id)

    return jsonify(response)


@roleRoutes.delete("/<int:id>/")
def delete(id: int):
    if id == 1:
        return jsonify({"message": "Acceso denegado"})

    obj = TROLE.query.get(id)
    if obj is None:
        return jsonify({"message": "Rol no encontrado"}), 400
    obj.state = "inactive"
    db.session.commit()

    return jsonify(obj.to_json())


@roleRoutes.put("/<int:id>/")
def update(id: int):
    if id == 1:
        return Response.fail("Acceso denegado"), 400

    json = request.json
    if json is None:
        return

    obj = TROLE.query.get(id)
    if obj is None:
        return Response.fail("Rol desconocido"), 400

    obj.from_json(json)
    db.session.commit()

    return Response.success("Rol actualizado correctamente", {})
