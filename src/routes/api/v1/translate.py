from flask import Blueprint, request
from models.response import Response

qq
translateRoutes = Blueprint('translate', __name__, url_prefix="/translate")


@translateRoutes.post('/')
def translate():
    photos = request.files

    return Response.new("Success")
