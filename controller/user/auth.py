import logging
from flask import jsonify, request, Blueprint
from flask_jwt_extended import create_access_token
from cerberus import Validator
from bugsnag.handlers import BugsnagHandler

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

logger = logging.getLogger(__name__)
handler = BugsnagHandler()

handler.setLevel(logging.ERROR)
logger.addHandler(handler)


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

        additional_claims = {}

        user_roles = result.user_roles
        roles = np.array([user_role.__dict__['role_id'] for user_role in user_roles]).flatten().tolist()
        additional_claims['roles'] = roles
        additional_claims['user_id'] = result.id

        gira_token = create_access_token(payload_model.username, additional_claims=additional_claims)

        response_model = UserAuthResponse(gira_token=gira_token)

        auth_response = response_model.__dict__

        return jsonify(auth_response), 200
    except Exception as e:
        error_model = ErrorResponse(errors='unknown error')
        error = error_model.__dict__
        logger.error(str(e))

        return jsonify(error), 500
