import json
from werkzeug.exceptions import BadRequest
from functools import wraps
from flask import jsonify
from flask import request

import jwt
from schema.error_schema import ErrorResponse
from constant import Constant as CONSTANT


def requires_gira_role(roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:

                token_raw = request.headers['AUTHORIZATION']
                token = token_raw.split()[1]
                user_data = jwt.decode(token, CONSTANT.JWT_SECRET_KEY, algorithms='HS256')

                roles_token = user_data['roles']

                """ reject if user doesn't have permission  """
                if not any(role in roles for role in roles_token):
                    message_model = ErrorResponse(
                        errors=[
                            'You don\'t have authorization to access this.'
                        ])
                    message = message_model.__dict__

                    return jsonify(message), 401

                return func(*args, **kwargs)
            except Exception as e:
                error_model = ErrorResponse(errors=[
                    'Authentication error.'
                ])
                error = error_model.__dict__
                return jsonify(error), 400

        return wrapper

    return decorator


def validate_request_input(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        try:
            """ Parse headers """
            request_method = request.method

            if request_method in ['POST', 'PATCH']:
                try:
                    payload = json.loads(request.data.decode())

                    if type(payload) != dict:
                        raise BadRequest

                    if request_method == 'PATCH':
                        if len(payload) == 0:
                            error_model = ErrorResponse(errors='Payload cannot be empty.')
                            error = error_model.__dict__

                            return jsonify(error), 400

                except (BadRequest, json.JSONDecodeError):
                    error_model = ErrorResponse(errors='Invalid JSON payload.')
                    error = error_model.__dict__

                    return jsonify(error), 400

            return func(*args, **kwargs)
        except Exception:
            message = {
                'info': {
                    'message': 'Authentication error',
                }
            }

            return jsonify(message), 400

    return decorated
