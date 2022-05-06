from flask import jsonify, Blueprint
from flask_jwt_extended import jwt_required

from helper.authentication_helper import validate_request_input, \
    requires_gira_role
from models.models import Issue, db
from sqlalchemy import and_
from sqlalchemy.sql.expression import false

from schema.error_schema import ErrorResponse
from schema.issue.issue_get_schema import IssueGetResponse

issue_get_endpoint = Blueprint('issue', __name__)


@issue_get_endpoint.route("issue/<issue_id>", methods=["GET"])
@validate_request_input
@jwt_required()
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

        return jsonify(error), 500
