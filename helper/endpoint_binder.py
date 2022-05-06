from flask import current_app

from controller.user.auth import user_auth_endpoint
from controller.user.register import user_register_endpoint

from controller.issue.issue_create import issue_create_endpoint
from controller.issue.issue_update import issue_update_endpoint
from controller.issue.issue_delete import issue_delete_endpoint

from controller.project.project_create import project_create_endpoint
from controller.project.project_delete import project_delete_endpoint
from controller.project.project_update import project_update_endpoint


def bind_endpoints():
    current_app.register_blueprint(user_auth_endpoint, url_prefix='/v1/')

    current_app.register_blueprint(user_register_endpoint, url_prefix='/v1/')

    current_app.register_blueprint(issue_create_endpoint, url_prefix='/v1/')
    current_app.register_blueprint(issue_update_endpoint, url_prefix='/v1/')
    current_app.register_blueprint(issue_delete_endpoint, url_prefix='/v1/')

    current_app.register_blueprint(project_create_endpoint, url_prefix='/v1/')
    current_app.register_blueprint(project_delete_endpoint, url_prefix='/v1/')
    current_app.register_blueprint(project_update_endpoint, url_prefix='/v1/')
