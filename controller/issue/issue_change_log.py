import logging
from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required
from cerberus import Validator
from bugsnag.handlers import BugsnagHandler

from helper.authentication_helper import validate_request_input, \
    requires_gira_role
from helper.format_helper import parse_cerberus_error_messages

from sqlalchemy import and_
from sqlalchemy.sql.expression import false
from models.models import Issue, IssueChangeLog, db

from schema.error_schema import ErrorResponse
from schema.info_schema import InfoResponse
from schema.issue.issue_change_log_schema import IssueChangeLogPostRequest, \
    ISSUE_CHANGE_LOG_POST_REQUEST_SCHEMA

from schema.issue.issue_log_get_schema import IssueLogGetResponse

issue_change_log_endpoint = Blueprint('issue_change_log', __name__)

logger = logging.getLogger(__name__)
handler = BugsnagHandler()

handler.setLevel(logging.ERROR)
logger.addHandler(handler)


@issue_change_log_endpoint.route("issue_change_log/<issue_id>", methods=["GET"])
@validate_request_input
@jwt_required()
@requires_gira_role(roles=[1, 2])
def issue_change_log_get_method(issue_id):
    try:

        issue_log_list = db.session.query(Issue, IssueChangeLog).join(IssueChangeLog).filter(
            and_(Issue.id == int(issue_id), Issue.is_deleted == false())).all()

        if not issue_log_list:
            error_model = ErrorResponse(errors=[
                'No issue log found'
            ])
            error = error_model.__dict__

            return jsonify(error), 404

        response_list = []

        for issue_item in issue_log_list:
            temp_object = {
                'id': issue_item.IssueChangeLog.id,
                'field_name': issue_item.IssueChangeLog.field_name,
                'new_value': issue_item.IssueChangeLog.new_value,
                'old_value': issue_item.IssueChangeLog.old_value,
                'user_id': issue_item.IssueChangeLog.user_id,
                'issue_id': issue_item.IssueChangeLog.issue_id,
                'created': issue_item.IssueChangeLog.created.strftime("%m/%d/%Y, %H:%M:%S"),
                'modified': issue_item.IssueChangeLog.modified.strftime("%m/%d/%Y, %H:%M:%S"),
            }
            response_list.append(temp_object)

        """ Result response model """
        response_model = IssueLogGetResponse(response_list)

        auth_response = response_model.__dict__

        return jsonify(auth_response), 200
    except Exception as e:
        error_model = ErrorResponse(errors='unknown error')
        error = error_model.__dict__
        logger.error(str(e))

        return jsonify(error), 500


@issue_change_log_endpoint.route("issue_change_log", methods=["POST"])
@validate_request_input
@jwt_required()
@requires_gira_role(roles=[1, 2])
def issue_change_log_post_method():
    try:
        """ Request body payload """
        payload = request.json
        payload_model = IssueChangeLogPostRequest(payload=payload)

        """ Validate payload """
        validator = Validator(ISSUE_CHANGE_LOG_POST_REQUEST_SCHEMA, allow_unknown=False)
        validation_result = validator.validate(payload)

        if not validation_result:
            error_message = parse_cerberus_error_messages(validator)
            error_model = ErrorResponse(errors=error_message)
            error = error_model.__dict__

            return jsonify(error), 400

        issue = db.session.query(Issue).filter(
            and_(Issue.id == int(payload_model.issue_id), Issue.is_deleted == false())).first()

        if not issue:
            error_model = ErrorResponse(errors=[
                'No issue found'
            ])
            error = error_model.__dict__

            return jsonify(error), 404

        issue_log = IssueChangeLog(issue_id=payload_model.issue_id,
                                   user_id=payload_model.user_id,
                                   new_value=payload_model.new_value,
                                   old_value=issue[payload_model.field_name],
                                   field_name=payload_model.field_name)

        issue[payload_model.field_name] = payload_model.new_value
        db.session.add(issue_log)
        db.session.commit()

        """ Result response model """
        response_model = InfoResponse()

        auth_response = response_model.__dict__

        return jsonify(auth_response), 201
    except Exception as e:
        error_model = ErrorResponse(errors='unknown error')
        error = error_model.__dict__
        logger.error(str(e))

        return jsonify(error), 500
