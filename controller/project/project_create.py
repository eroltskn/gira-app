from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required
from cerberus import Validator

from helper.authentication_helper import validate_request_input, \
    requires_gira_role
from helper.format_helper import parse_cerberus_error_messages

from models.models import Project, db

from schema.error_schema import ErrorResponse
from schema.info_schema import InfoResponse
from schema.project.project_create_schema import ProjectPostRequest, \
    PROJECT_POST_REQUEST_SCHEMA

project_create_endpoint = Blueprint('project/create', __name__)


@project_create_endpoint.route("project/create", methods=["POST"])
@validate_request_input
@jwt_required()
@requires_gira_role(roles=[1])
def project_post_method():
    try:
        """ Request body payload """
        payload = request.json
        payload_model = ProjectPostRequest(payload=payload)

        """ Validate payload """
        validator = Validator(PROJECT_POST_REQUEST_SCHEMA, allow_unknown=False)
        validation_result = validator.validate(payload)

        if not validation_result:
            error_message = parse_cerberus_error_messages(validator)
            error_model = ErrorResponse(errors=error_message)
            error = error_model.__dict__

            return jsonify(error), 400

        project = Project(name=payload_model.name,
                          assign_by=payload_model.assign_by,
                          assign_to=payload_model.assign_by
                          )

        db.session.add(project)
        db.session.commit()

        """ Result response model """
        response_model = InfoResponse()

        auth_response = response_model.__dict__

        return jsonify(auth_response), 200
    except Exception as e:
        error_model = ErrorResponse(errors='unknown error')
        error = error_model.__dict__

        return jsonify(error), 500
