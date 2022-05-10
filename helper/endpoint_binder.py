from flask import current_app

from controller.user.auth import user_auth_endpoint
from controller.user.register import user_register_endpoint

from controller.project.project_api import project_api_endpoint
from controller.issue.issue_api import issue_api_endpoint
from controller.issue.issue_change_log import issue_change_log_endpoint


def bind_endpoints():
    current_app.register_blueprint(user_auth_endpoint, url_prefix='/v1/')

    current_app.register_blueprint(user_register_endpoint, url_prefix='/v1/')

    current_app.register_blueprint(project_api_endpoint, url_prefix='/v1/')
    current_app.register_blueprint(issue_api_endpoint, url_prefix='/v1/')
    current_app.register_blueprint(issue_change_log_endpoint, url_prefix='/v1/')
