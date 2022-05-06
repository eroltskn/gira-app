from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required
from cerberus import Validator

from helper.authentication_helper import validate_request_input, \
    requires_gira_role
from helper.format_helper import parse_cerberus_error_messages

from models.models import Project,Issue, db

from schema.error_schema import ErrorResponse
from schema.info_schema import InfoResponse
from schema.project.project_update_schema import PROJECT_PATCH_REQUEST_SCHEMA, ProjectPatchRequest

project_delete_endpoint = Blueprint('project/delete', __name__)


@project_delete_endpoint.route("project/delete/<project_id>", methods=["DELETE"])
@validate_request_input
@jwt_required()
@requires_gira_role(roles=[1, 2])
def project_post_method(project_id):
    try:
        project = Project.query.get(project_id)

        project.is_deleted = True

        db.session.query(Issue).filter(Issue.project_id == project_id).update({'is_deleted': True})

        db.session.commit()

        """ Result response model """
        response_model = InfoResponse()

        auth_response = response_model.__dict__

        return jsonify(auth_response), 200
    except Exception as e:
        error_model = ErrorResponse(errors='unknown error')
        error = error_model.__dict__

        return jsonify(error), 500
