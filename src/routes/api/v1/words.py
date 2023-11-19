from flask import Blueprint, jsonify, request

from src.models.word import TWORD
from src.models.response import Response
from src.utils.validators import is_valid_json_word
from src.database.db import db


wordsRoutes = Blueprint("words", __name__, url_prefix="/words")


@wordsRoutes.get("/")
def get_all():
    words = TWORD.query.all()
    return Response.new("Lista de palabras", data=[word.to_json() for word in words])


@wordsRoutes.post("/")
def create():
    json = request.json

    if not is_valid_json_word(json):
        return jsonify({"message": "Petición incorrecta"}), 400

    new = TWORD().from_json(json)

    db.session.add(new)
    db.session.commit()

    return jsonify(new.to_json())


@wordsRoutes.get("/<int:id>")
def get_by_id(id: int):
    obj = TWORD.query.get(id)
    if obj is None or obj.state == "inactive":
        return jsonify({"message": "Palabra no encontrado"}), 400

    response = obj.to_json()

    return jsonify(response)


@wordsRoutes.delete("/<int:id>")
def delete(id: int):
    obj = TWORD.query.get(id)
    if obj is None:
        return jsonify({"message": "Palabra no encontrado"}), 400
    obj.state = "inactive"
    db.session.commit()

    return jsonify(obj.to_json())


@wordsRoutes.put("/<int:id>")
def update(id: int):
    json = request.json
    if not is_valid_json_word(json):
        return jsonify({"message": "Petición incorrecta"}), 400

    obj = TWORD.query.get(id)
    if obj is None:
        return jsonify({"message": "Palabra no encontrado"}), 400

    obj.from_json(json)
    db.session.commit()

    return jsonify(obj.to_json())
