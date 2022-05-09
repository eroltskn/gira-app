import logging
from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required
from cerberus import Validator
from bugsnag.handlers import BugsnagHandler

from models.models import Project, Issue, UserProject, db
from sqlalchemy import and_
from sqlalchemy.sql.expression import false
from sqlalchemy import func

from helper.authentication_helper import validate_request_input, \
    requires_gira_role
from helper.format_helper import parse_cerberus_error_messages

from schema.error_schema import ErrorResponse
from schema.info_schema import InfoResponse

from schema.project.project_assign_schema import ProjectAssignPostRequest,\
    PROJECT_ASSIGN_POST_REQUEST_SCHEMA
from schema.project.project_create_schema import ProjectPostRequest, \
    PROJECT_POST_REQUEST_SCHEMA
from schema.project.project_get_schema import ProjectGetResponse
from schema.project.project_update_schema import ProjectPatchRequest,\
    PROJECT_PATCH_REQUEST_SCHEMA

project_api_endpoint = Blueprint('project', __name__)

logger = logging.getLogger(__name__)
handler = BugsnagHandler()

handler.setLevel(logging.ERROR)
logger.addHandler(handler)


@project_api_endpoint.route("project/<project_id>", methods=["GET"])
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

        issue_count = db.session.query(func.count(Issue.id)).filter(
            and_(Issue.project_id == project_id, Issue.is_deleted == false())).scalar()

        response_object = {
            'id': project.id,
            'name': project.name,
            'created_by': project.created_by,
            'issue_count': issue_count,
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

        logger.error(str(e))

        return jsonify(error), 500


@project_api_endpoint.route("project", methods=["POST"])
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
                          created_by=payload_model.created_by,
                          )

        db.session.add(project)
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


@project_api_endpoint.route("project/<project_id>", methods=["PATCH"])
@validate_request_input
@jwt_required()
@requires_gira_role(roles=[1, 2])
def project_update_method(project_id):
    try:
        """ Request body payload """
        payload = request.json
        payload_model = ProjectPatchRequest(payload=payload)

        """ Validate payload """
        validator = Validator(PROJECT_PATCH_REQUEST_SCHEMA, allow_unknown=False)
        validation_result = validator.validate(payload)

        if not validation_result:
            error_message = parse_cerberus_error_messages(validator)
            error_model = ErrorResponse(errors=error_message)
            error = error_model.__dict__

            return jsonify(error), 400

        project = Project.query.get(project_id)

        if payload_model.name:
            project.name = payload_model.name

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


@project_api_endpoint.route("project/<project_id>", methods=["DELETE"])
@validate_request_input
@jwt_required()
@requires_gira_role(roles=[1, 2])
def project_delete_method(project_id):
    try:
        project = Project.query.get(project_id)

        """ Check row if row exists """
        if not project:
            error_model = ErrorResponse(errors=[
                'No project found'
            ])
            error = error_model.__dict__

            return jsonify(error), 404

        project.is_deleted = True
        db.session.query(Issue).filter(Issue.project_id == project_id).update({'is_deleted': True})

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


@project_api_endpoint.route("project/assign", methods=["POST"])
@validate_request_input
@jwt_required()
@requires_gira_role(roles=[1])
def project_assign_post_method():
    try:
        """ Request body payload """
        payload = request.json
        payload_model = ProjectAssignPostRequest(payload=payload)

        """ Validate payload """
        validator = Validator(PROJECT_ASSIGN_POST_REQUEST_SCHEMA, allow_unknown=False)
        validation_result = validator.validate(payload)

        if not validation_result:
            error_message = parse_cerberus_error_messages(validator)
            error_model = ErrorResponse(errors=error_message)
            error = error_model.__dict__

            return jsonify(error), 400

        project = UserProject(user_id=payload_model.user_id,
                              project_id=payload_model.project_id)

        db.session.add(project)
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
