from flask import jsonify, request
import jwt
from sqlalchemy.util.deprecations import os

from models.user import TUSER
from utils.roles import get_permissions_of_role


def check_jwt(token):
    try:
        payload = jwt.decode(token, os.getenv("JWT_KEY"), algorithms=['HS256'])
        return None, payload['user']
    except jwt.ExpiredSignatureError:
        return 'Token JWT expirado', None
    except jwt.InvalidTokenError:
        return 'Token JWT inválido', None


def check_permissions(module, permissions):
    token = request.headers.get('Authorization')

    if not token:
        return jsonify({'message': 'Token JWT faltante'}), 401

    res, code = check_jwt(token)

    if res is not None:
        return False, res

    user = TUSER.query.get(code)

    if not user:
        return False, "Usuario desconocido"

    permissions_of_user = get_permissions_of_role(
        user.role_id).get(module)

    if not permissions_of_user or not all(elem in permissions_of_user for elem in permissions):
        return False, "No autorizado"

    return True, "Success"
