import jwt
import os

from flask import Blueprint, request
from werkzeug.security import generate_password_hash
from src.models.response import Response
from src.models.user import TUSER
from src.services.auth_service import AuthService
from src.database.db import db

from src.utils.roles import get_permissions_of_role
from src.utils.validators import is_valid_json_login


authRoutes = Blueprint("auth", __name__, url_prefix="/auth")


@authRoutes.post("/login")
def login():
    login_json = request.json

    if login_json is None or not is_valid_json_login(login_json):
        return Response.new("Petición incorrecta", success=False), 400

    user = TUSER.query.filter_by(email=login_json["email"]).first()

    if user is None or not user.is_correct_password(login_json["password"]):
        return Response.new("usuario o contraseña incorrecto", False), 400

    if user.state != "active":
        return Response.new("usuario deshabilitado", success=False), 400

    token = AuthService().generate_token(user)
    print(token)
    user = user.to_json()
    user["token"] = token
    user["permissions"] = get_permissions_of_role(user.get("role"))

    return Response.new("Inicio de sesión correcto", data=user)


@authRoutes.post("/verify")
def verify_token():
    if request.json is None or not request.json.token:
        return Response.new("Token invalido", success=False), 400

    if not AuthService().verify_token(request.json.token):
        return Response.new("Token invalido", success=False), 400

    return Response.new("Token valido")


@authRoutes.post("/password_reset/<string:token>")
def password_reset(token):
    try:
        payload = jwt.decode(token, os.getenv("JWT_KEY"), algorithms=["HS256"])
    except Exception:
        return Response.fail("Codigo inválido"), 400

    user: TUSER = TUSER.query.get(payload["id"])
    if user is None:
        return Response.fail("Usuario no encontrado"), 400

    json_user = request.json
    if not json_user:
        return Response.fail("Petición incorrecta"), 400

    user.password = json_user["password"]
    db.session.commit()

    return Response.new("Cambio de contraseña correcto")


@authRoutes.post("/confirm/<int:id>")
def confirm_account(id):
    user: TUSER = TUSER.query.get(id)
    if user is None:
        return Response.fail("Usuario no encontrado"), 400

    if user.password is None:
        return Response.fail("Usuario no encontrado"), 400

    json_user = request.json
    if not json_user:
        return Response.fail("Petición incorrecta"), 400

    passwd = json_user["password"]

    user.password = passwd
    db.session.commit()

    return Response.new("Cuenta creada correctamente")


@authRoutes.get("/hash/<string:passw>")
def hash_test(passw: str):
    return generate_password_hash(passw, method="sha256")
