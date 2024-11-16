from flask import Blueprint, request

from src.models.word import TWORD
from src.models.response import Response
from src.database.db import db


wordsRoutes = Blueprint("words", __name__, url_prefix="/words")


# @wordsRoutes.get("/test")
# def get_test():
#     words = TWORD.query.filter(
#         TWORD.state.ilike("active"),
#     ).all()
#
#     return Response.new("Lista de palabras", data=[word.to_json() for word in words])


@wordsRoutes.get("/")
def get_all():
    search_param = request.args.get("search")
    status = request.args.get("status")
    words = db.session.query(TWORD)

    if search_param:
        words = words.filter(TWORD.word.ilike(f"%{search_param}%"))

    if status:
        words = words.filter(TWORD.state == status)

    words_json = [word.to_json() for word in words.all()]

    return Response.new("Lista de palabras", data=words_json)


@wordsRoutes.post("/")
def create():
    json = request.json

    # if not is_valid_json_word(json):
    #     return jsonify({"message": "Petición incorrecta"}), 400

    new = TWORD().from_json(json)

    db.session.add(new)
    db.session.commit()

    return Response.success("Palabra creada correctamente", new.to_json())


@wordsRoutes.get("/<int:id>/")
def get_by_id(id: int):
    obj = TWORD.query.get(id)
    if obj is None or obj.state == "inactive":
        return Response.fail("Palabra no encontrada"), 400

    response = obj.to_json()

    return Response.success("Palabra", response)


@wordsRoutes.delete("/<int:id>/")
def delete(id: int):
    obj = TWORD.query.get(id)
    if obj is None:
        return Response.fail("Palabra no encontrado"), 400
    obj.state = "inactive"
    db.session.commit()

    return Response.success("Palabra eliminada correctamente", obj.to_json())


@wordsRoutes.put("/<int:id>/")
def update(id: int):
    json = request.json
    # if not is_valid_json_word(json):
    #     return jsonify({"message": "Petición incorrecta"}), 400

    obj = TWORD.query.get(id)
    if obj is None:
        return Response.fail("Palabra no encontrado"), 400

    obj.from_json(json)
    db.session.commit()

    return Response.success("Palabra actualizada correctamente", obj.to_json())
