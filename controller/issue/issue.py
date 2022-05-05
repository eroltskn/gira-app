from flask import jsonify, request, Blueprint
from flask_jwt_extended import create_access_token, jwt_required
from flask_jwt_extended import get_jwt
from flask_jwt_extended import get_jwt_identity
from cerberus import Validator

from helper.authentication_helper import validate_request_input, \
    requires_gira_role
from helper.format_helper import parse_cerberus_error_messages

from models.models import Issue, Project, db

from schema.error_schema import ErrorResponse
from schema.info_schema import InfoResponse
from schema.issue.issue_schema import ISSUE_POST_REQUEST_SCHEMA
from schema.issue.issue_schema import IssuePostRequest
from schema.user.user_register_schema import UserRegisterResponse

issue_endpoint = Blueprint('issue', __name__)


@issue_endpoint.route("issue", methods=["POST"])
@validate_request_input
@jwt_required()
@requires_gira_role(roles=[1])
def issue_post_method():
    try:
        """ Request body payload """
        payload = request.json
        payload_model = IssuePostRequest(payload=payload)

        """ Validate payload """
        validator = Validator(ISSUE_POST_REQUEST_SCHEMA, allow_unknown=False)
        validation_result = validator.validate(payload)

        if not validation_result:
            error_message = parse_cerberus_error_messages(validator)
            error_model = ErrorResponse(errors=error_message)
            error = error_model.__dict__

            return jsonify(error), 400

        issue = Issue(name=payload_model.name,
                      description=payload_model.description,
                      issue_status_id=payload_model.issue_status_id,
                      issue_type_id=payload_model.issue_type_id,
                      project_id=payload_model.project_id)

        db.session.add(issue)

        project = Project.query.get(payload_model.project_id)

        project.issue_count += 1

        db.session.commit()

        """ Result response model """
        response_model = InfoResponse()

        auth_response = response_model.__dict__

        return jsonify(auth_response), 200
    except Exception as e:
        error_model = ErrorResponse(errors='unknown error')
        error = error_model.__dict__

        return jsonify(error), 500
