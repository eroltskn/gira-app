from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required
from cerberus import Validator

from helper.authentication_helper import validate_request_input, \
    requires_gira_role
from helper.format_helper import parse_cerberus_error_messages

from models.models import Issue, db

from schema.error_schema import ErrorResponse
from schema.info_schema import InfoResponse
from schema.issue.issue_update_schema import IssuePatchRequest, \
    ISSUE_PATCH_REQUEST_SCHEMA

issue_update_endpoint = Blueprint('issue/update', __name__)


@issue_update_endpoint.route("issue/update/<issue_id>", methods=["PATCH"])
@validate_request_input
@jwt_required()
@requires_gira_role(roles=[1, 2])
def issue_patch_method(issue_id):
    try:
        """ Request body payload """
        payload = request.json
        payload_model = IssuePatchRequest(payload=payload)

        """ Validate payload """
        validator = Validator(ISSUE_PATCH_REQUEST_SCHEMA, allow_unknown=False)
        validation_result = validator.validate(payload)

        if not validation_result:
            error_message = parse_cerberus_error_messages(validator)
            error_model = ErrorResponse(errors=error_message)
            error = error_model.__dict__

            return jsonify(error), 400

        issue = Issue.query.get(issue_id)

        if payload_model.name:
            issue.name = payload_model.name

        if payload_model.description:
            issue.description = payload_model.description

        if payload_model.issue_type_id:
            issue.issue_type_id = payload_model.issue_type_id

        if payload_model.issue_status_id:
            issue.issue_status_id = payload_model.issue_status_id

        db.session.commit()

        """ Result response model """
        response_model = InfoResponse()

        auth_response = response_model.__dict__

        return jsonify(auth_response), 200
    except Exception as e:
        error_model = ErrorResponse(errors='unknown error')
        error = error_model.__dict__

        return jsonify(error), 500
