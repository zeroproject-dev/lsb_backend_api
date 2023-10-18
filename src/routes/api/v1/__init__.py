from flask import Blueprint
from .users import usersRoutes
from .auth import authRoutes
from .role import roleRoutes
from .video import videosRoutes
from .words import wordsRoutes
from .permissions import permissionRoute
from .translate import translateRoutes

v1 = Blueprint('v1', __name__, url_prefix="/v1")

v1.register_blueprint(usersRoutes)
v1.register_blueprint(authRoutes)
v1.register_blueprint(roleRoutes)
v1.register_blueprint(videosRoutes)
v1.register_blueprint(wordsRoutes)
v1.register_blueprint(permissionRoute)
v1.register_blueprint(translateRoutes)
