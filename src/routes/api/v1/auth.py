from flask import Blueprint, jsonify, request
from models.response import Response
from models.user import TUSER
from services.auth_service import AuthService

from utils.roles import get_permissions_of_role
from utils.validators import is_valid_json_login


authRoutes = Blueprint('auth', __name__, url_prefix="/auth")


@authRoutes.post('/login')
def login():
    login_json = request.json

    if login_json is None or not is_valid_json_login(login_json):
        return Response.new("Petición incorrecta", False), 400

    user = TUSER.query.filter_by(email=login_json['email']).first()

    if user is None or not user.is_correct_password(login_json['password']):
        return Response.new("usuario o contraseña incorrecto", False), 400

    if user.state != 'active':
        return Response.new("usuario deshabilitado", False), 400

    token = AuthService().generate_token(user)
    user = user.to_json()
    user['token'] = token
    user['permissions'] = get_permissions_of_role(user.get('role'))

    return Response.new("Inicio de sesión correcto", data=user)


@ authRoutes.post('/logout')
def logout():
    return jsonify({"AUTH": "HELLO"})
