import logging
import json
from werkzeug.exceptions import BadRequest

from functools import wraps
from flask import jsonify
from flask import request
from flask_jwt_extended import get_jwt
from schema.error_schema import ErrorResponse

logger = logging.getLogger(__name__)


def requires_gira_role(roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                claims = get_jwt()

                return func(*args, **kwargs)
            except Exception:
                return jsonify('not allowed'), 400

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
