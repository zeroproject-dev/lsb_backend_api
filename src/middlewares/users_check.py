from ..middlewares.jwt import check_permissions


def check_users_permissions(permissions):
    return check_permissions("usuarios", permissions)


def check_users_list():
    return check_users_permissions(["listar usuarios"])


def check_users_register():
    return check_users_permissions(["agregar usuario"])


def check_users_modify():
    return check_users_permissions(["modificar usuario"])


def check_users_delete():
    return check_users_permissions(["eliminar usuario"])
