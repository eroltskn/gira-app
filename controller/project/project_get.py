from flask import jsonify, Blueprint
from flask_jwt_extended import jwt_required

from helper.authentication_helper import validate_request_input, \
    requires_gira_role
from models.models import Project, db
from sqlalchemy import and_
from sqlalchemy.sql.expression import false

from schema.error_schema import ErrorResponse
from schema.project.project_get_schema import ProjectGetResponse

project_get_endpoint = Blueprint('project', __name__)


@project_get_endpoint.route("project/<project_id>", methods=["GET"])
@validate_request_input
@jwt_required()
@requires_gira_role(roles=[1, 2])
def project_get_method(project_id):
    try:
        project = db.session.query(Project).filter(
            and_(Project.id == project_id, Project.is_deleted == false())).first()

        """ Check row if row exists """
        if not project:
            error_model = ErrorResponse(errors=[
                'No project found'
            ])
            error = error_model.__dict__

            return jsonify(error), 404

        response_object = {
            'id': project.id,
            'name': project.name,
            'created_by': project.created_by,
            'issue_count': project.issue_count,
            'created': project.created.strftime("%m/%d/%Y, %H:%M:%S"),
            'modified': project.modified.strftime("%m/%d/%Y, %H:%M:%S"),
        }
        """ Result response model """
        response_model = ProjectGetResponse(response_object)

        auth_response = response_model.__dict__

        return jsonify(auth_response), 200
    except Exception as e:
        error_model = ErrorResponse(errors='unknown error')
        error = error_model.__dict__

        return jsonify(error), 500
