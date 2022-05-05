from flask import jsonify, request, Blueprint
from flask_jwt_extended import create_access_token
from cerberus import Validator
from sqlalchemy import and_

from helper.authentication_helper import validate_request_input
from helper.format_helper import parse_cerberus_error_messages
from models.models import User, db
from schema.error_schema import ErrorResponse
from schema.user.user_auth_schema import UserAuthPostRequest, \
    USER_AUTH_POST_REQUEST_SCHEMA, \
    UserAuthResponse
import numpy as np

user_auth_endpoint = Blueprint('login', __name__)


@user_auth_endpoint.route("login", methods=["POST"])
@validate_request_input
def login():
    try:
        """ Request body payload """
        payload = request.json
        payload_model = UserAuthPostRequest(payload=payload)

        """ Validate payload """
        validator = Validator(USER_AUTH_POST_REQUEST_SCHEMA, allow_unknown=False)
        validation_result = validator.validate(payload)

        if not validation_result:
            error_message = parse_cerberus_error_messages(validator)
            error_model = ErrorResponse(errors=error_message)
            error = error_model.__dict__

            return jsonify(error), 400

        result = db.session.query(User).filter(
            and_(User.username == payload_model.username, User.password == payload_model.password)).first()

        """ Check authentication is success """
        if not result:
            error_model = ErrorResponse(errors=[
                'Authentication error.'
            ])
            error = error_model.__dict__

            return jsonify(error), 401

        result_dict = result.__dict__
        additional_claims = {}

        if 'user_roles' in result_dict:
            user_roles = result_dict['user_roles']
            roles = np.array([user_role.__dict__['role_id'] for user_role in user_roles]).flatten().tolist()
            additional_claims['roles'] = roles

        gira_token = create_access_token(result_dict['username'], additional_claims=additional_claims)

        response_model = UserAuthResponse(gira_token=gira_token)

        auth_response = response_model.__dict__

        return jsonify(auth_response), 200
    except Exception as e:
        error_model = ErrorResponse(errors='unknown error')
        error = error_model.__dict__

        return jsonify(error), 500