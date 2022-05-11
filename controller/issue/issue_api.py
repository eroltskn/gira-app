import logging
from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required
from cerberus import Validator
from bugsnag.handlers import BugsnagHandler

from helper.authentication_helper import validate_request_input, \
    requires_gira_role, requires_owner_role
from helper.format_helper import parse_cerberus_error_messages

from sqlalchemy import and_
from sqlalchemy.sql.expression import false
from models.models import Issue, Project, db

from schema.error_schema import ErrorResponse
from schema.info_schema import InfoResponse
from schema.issue.issue_create_schema import ISSUE_POST_REQUEST_SCHEMA
from schema.issue.issue_create_schema import IssuePostRequest
from schema.issue.issue_get_schema import IssueGetResponse
from schema.issue.issue_update_schema import IssuePatchRequest, ISSUE_PATCH_REQUEST_SCHEMA

issue_api_endpoint = Blueprint('issue', __name__)

logger = logging.getLogger(__name__)
handler = BugsnagHandler()

handler.setLevel(logging.ERROR)
logger.addHandler(handler)


@issue_api_endpoint.route("issue/<issue_id>", methods=["GET"])
@validate_request_input
@jwt_required()
@requires_owner_role
@requires_gira_role(roles=[1, 2])
def issue_get_method(issue_id):
    try:

        issue = db.session.query(Issue).filter(
            and_(Issue.id == int(issue_id), Issue.is_deleted == false())).first()

        if not issue:
            error_model = ErrorResponse(errors=[
                'No issue found'
            ])
            error = error_model.__dict__

            return jsonify(error), 404

        response_object = {
            'id': issue.id,
            'name': issue.name,
            'description': issue.description,
            'project_id': issue.project_id,
            'issue_status_id': issue.issue_status_id,
            'issue_type_id': issue.issue_type_id,
            'created': issue.created.strftime("%m/%d/%Y, %H:%M:%S"),
            'modified': issue.modified.strftime("%m/%d/%Y, %H:%M:%S"),
        }

        """ Result response model """
        response_model = IssueGetResponse(response_object)

        auth_response = response_model.__dict__

        return jsonify(auth_response), 200
    except Exception as e:
        error_model = ErrorResponse(errors='unknown error')
        error = error_model.__dict__
        logger.error(str(e))

        return jsonify(error), 500


@issue_api_endpoint.route("issue", methods=["POST"])
@jwt_required()
@validate_request_input
@requires_owner_role
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
        db.session.commit()

        """ Result response model """
        response_model = InfoResponse()

        auth_response = response_model.__dict__

        return jsonify(auth_response), 200
    except Exception as e:
        error_model = ErrorResponse(errors='unknown error')
        error = error_model.__dict__
        logger.error(str(e))

        return jsonify(error), 500


@issue_api_endpoint.route("issue/<issue_id>", methods=["PATCH"])
@validate_request_input
@jwt_required()
@requires_owner_role
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
        logger.error(str(e))

        return jsonify(error), 500


@issue_api_endpoint.route("issue/<issue_id>", methods=["DELETE"])
@validate_request_input
@jwt_required()
@requires_owner_role
@requires_gira_role(roles=[1, 2])
def issue_delete_method(issue_id):
    try:

        issue = Issue.query.get(issue_id)

        """ Check row if row exists """
        if not issue:
            error_model = ErrorResponse(errors=[
                'No project found'
            ])
            error = error_model.__dict__

            return jsonify(error), 404

        # soft deletion
        issue.is_deleted = True

        db.session.commit()

        """ Result response model """
        response_model = InfoResponse()

        auth_response = response_model.__dict__

        return jsonify(auth_response), 204
    except Exception as e:
        error_model = ErrorResponse(errors='unknown error')
        error = error_model.__dict__
        logger.error(str(e))

        return jsonify(error), 500
