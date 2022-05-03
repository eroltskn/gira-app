from flask import jsonify, request, Blueprint
from flask_jwt_extended import create_access_token
from cerberus import Validator
from helper.authentication_helper import validate_request_input
from helper.format_helper import parse_cerberus_error_messages
from models.models import User, UserRole, UserProfile, db
from schema.error_schema import ErrorResponse
from schema.user.user_register_schema import USER_REGISTER_POST_REQUEST_SCHEMA
from schema.user.user_register_schema import UserRegisterResponse, \
    UserRegisterPostRequest

user_register_endpoint = Blueprint('register', __name__)


@user_register_endpoint.route("register", methods=["POST"])
@validate_request_input
def login():
    try:
        """ Request body payload """
        payload = request.json
        payload_model = UserRegisterPostRequest(payload=payload)

        """ Validate payload """
        validator = Validator(USER_REGISTER_POST_REQUEST_SCHEMA, allow_unknown=False)
        validation_result = validator.validate(payload)

        if not validation_result:
            error_message = parse_cerberus_error_messages(validator)
            error_model = ErrorResponse(errors=error_message)
            error = error_model.__dict__

            return jsonify(error), 400

        user = User(username=payload_model.username,
                    password=payload_model.password)

        db.session.add(user)
        db.session.flush()
        db.session.refresh(user)

        user_profile = UserProfile(user_id=user.id,
                                   email=payload_model.email,
                                   first_name=payload_model.first_name,
                                   last_name=payload_model.last_name)

        db.session.add(user_profile)
        user_role = UserRole(user_id=user.id,
                             role_id=1)

        db.session.add(user_role)
        db.session.commit()

        gira_token = create_access_token(payload_model.username, additional_claims={'roles': [1]})

        response_model = UserRegisterResponse(gira_token=gira_token)

        auth_response = response_model.__dict__

        return jsonify(auth_response), 200
    except Exception as e:
        error_model = ErrorResponse(errors='unknown error')
        error = error_model.__dict__

        return jsonify(error), 500
