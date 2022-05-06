from flask import jsonify,  Blueprint
from flask_jwt_extended import jwt_required

from helper.authentication_helper import validate_request_input, \
    requires_gira_role

from models.models import Issue, db
from schema.error_schema import ErrorResponse
from schema.info_schema import InfoResponse


issue_delete_endpoint = Blueprint('issue/delete', __name__)


@issue_delete_endpoint.route("issue/delete/<issue_id>", methods=["DELETE"])
@validate_request_input
@jwt_required()
@requires_gira_role(roles=[1, 2])
def issue_delete_method(issue_id):
    try:

        issue = Issue.query.get(issue_id)
        issue.is_deleted = True
        db.session.commit()

        """ Result response model """
        response_model = InfoResponse()

        auth_response = response_model.__dict__

        return jsonify(auth_response), 200
    except Exception as e:
        error_model = ErrorResponse(errors='unknown error')
        error = error_model.__dict__

        return jsonify(error), 500
