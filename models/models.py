"""Data models."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class UserRole(db.Model):
    """Data model for user role."""

    __tablename__ = "user_role"
    role_id = db.Column(db.Integer,
                        db.ForeignKey("role.id"),
                        primary_key=True)

    user_id = db.Column(db.Integer,
                        db.ForeignKey("user.id"),
                        primary_key=True)

    def __init__(self, role_id, user_id):
        self.role_id = role_id
        self.user_id = user_id


class UserProfile(db.Model):
    """Data model for user profile ."""

    __tablename__ = "user_profile"
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    user_id = db.Column(db.Integer,
                        db.ForeignKey("user.id"),
                        primary_key=False)

    email = db.Column(db.String(45),
                      index=False,
                      unique=True,
                      nullable=False)

    first_name = db.Column(db.String(45),
                           index=False,
                           unique=True,
                           nullable=False)

    last_name = db.Column(db.String(45),
                          index=False,
                          unique=True,
                          nullable=False)

    created = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(), nullable=False)
    modified = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(),
                         onupdate=db.func.current_timestamp(), nullable=False)

    def __init__(self, user_id, email, first_name, last_name):
        self.user_id = user_id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name


class User(db.Model):
    """Data model for user ."""

    __tablename__ = "user"
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    username = db.Column(db.String(45),
                         index=False,
                         unique=True,
                         nullable=False)
    password = db.Column(db.String(45),
                         index=False,
                         unique=False,
                         nullable=False)

    user_roles = db.relationship(UserRole,
                                 backref='user',
                                 lazy=True)

    user_profile = db.relationship(UserProfile,
                                   backref='user',
                                   lazy=True)

    def __init__(self, username, password):
        self.username = username
        self.password = password


class Role(db.Model):
    """Data model for role."""

    __tablename__ = "role"
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.String(45),
                     index=False,
                     unique=True,
                     nullable=False)

    user_role = db.relationship(UserRole,
                                backref='role',
                                lazy=True)


class Issue(db.Model):
    """Data model for issue."""

    __tablename__ = "issue"
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    name = db.Column(db.String(45),
                     index=False,
                     unique=True,
                     nullable=False)

    project_id = db.Column(db.Integer,
                           db.ForeignKey("project.id"),
                           nullable=False)


class Project(db.Model):
    """Data model for project"""

    __tablename__ = "project"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    name = db.Column(db.String(45),
                     index=False,
                     unique=True,
                     nullable=False)

    issues = db.relationship(Issue,
                             backref='project',
                             lazy=True)
