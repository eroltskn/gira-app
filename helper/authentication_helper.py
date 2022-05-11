import json
from werkzeug.exceptions import BadRequest
from functools import wraps
from flask import jsonify
from flask import request

import jwt
from schema.error_schema import ErrorResponse
from constant import Constant as CONSTANT

from sqlalchemy import and_
from sqlalchemy.sql.expression import false
from models.models import Issue, Project, UserProject, db


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
                if not any(role in roles_token for role in roles):
                    message_model = ErrorResponse(
                        errors=[
                            'You don\'t have authorization to access this endpoint'
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


def requires_owner_role(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            """ Parse headers """
            request_method = request.method

            token_raw = request.headers['AUTHORIZATION']
            token = token_raw.split()[1]
            user_data = jwt.decode(token, CONSTANT.JWT_SECRET_KEY, algorithms='HS256')

            roles_token = user_data['roles']
            user_id = user_data['user_id']

            issue_id = None
            project_id = None
            payload = request.json

            if request_method == 'POST' or request_method == 'PATCH':
                if 'project_id' in payload:
                    project_id = int(payload['project_id'])

                if 'issue_id' in payload:
                    issue_id = int(payload['issue_id'])

            if 'project_id' in kwargs:
                project_id = int(kwargs['project_id'])

            if 'issue_id' in kwargs:
                issue_id = int(kwargs['issue_id'])

            if project_id:

                # check for project creator user
                admin_user_check = db.session.query(Project).filter(
                    and_(Project.id == project_id, Project.created_by == user_id,
                         Project.is_deleted == false())).first()

                if admin_user_check:
                    return func(*args, **kwargs)

                # check for project assigned user
                assigned_user_check = db.session.query(UserProject, Project).join(Project).filter(
                    and_(UserProject.project_id == project_id, UserProject.user_id == user_id,
                         Project.is_deleted == false())).first()

                if not assigned_user_check:
                    message_model = ErrorResponse(
                        errors=[
                            'You don\'t have authorization to access this endpoint'
                        ])
                    message = message_model.__dict__

                    return jsonify(message), 401

            if issue_id:
                # check for project creator user
                admin_user_check = db.session.query(Project, Issue).join(Issue).filter(
                    and_(Project.created_by == user_id,
                         Issue.id == issue_id,
                         Project.is_deleted == false(),
                         Issue.is_deleted == false()
                         )).first()

                if admin_user_check:
                    return func(*args, **kwargs)

                # check for project creator user
                assigned_user_check = db.session.query(Project, UserProject, Issue).join(UserProject).join(Issue).filter(
                    and_(UserProject.user_id == user_id,
                         Issue.id == issue_id,
                         Project.is_deleted == false(),
                         Issue.is_deleted == false()
                         )).all()

                if not assigned_user_check:
                    message_model = ErrorResponse(
                        errors=[
                            'You don\'t have authorization to access this endpoint'
                        ])
                    message = message_model.__dict__

                    return jsonify(message), 401

            return func(*args, **kwargs)
        except Exception as e:
            message_model = ErrorResponse(errors=[
                'Authentication error.'
            ])

            message = message_model.__dict__

            return jsonify(message), 400

    return wrapper


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
