from flask import current_app

from controller.user.auth import user_auth_endpoint
from controller.user.register import user_register_endpoint

def bind_endpoints():
    current_app.register_blueprint(user_auth_endpoint, url_prefix='/v1/')
    current_app.register_blueprint(user_register_endpoint, url_prefix='/v1/')


