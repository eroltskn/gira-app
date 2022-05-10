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
                     unique=False,
                     nullable=False)

    description = db.Column(db.Text(),
                            unique=False,
                            nullable=False)

    is_deleted = db.Column(db.Boolean,
                           default=False)

    issue_status_id = db.Column(db.Integer,
                                db.ForeignKey("issue_status.id"),
                                nullable=False)

    issue_type_id = db.Column(db.Integer,
                              db.ForeignKey("issue_type.id"),
                              nullable=False)

    project_id = db.Column(db.Integer,
                           db.ForeignKey("project.id"),
                           nullable=False)

    project = db.relationship("Project",
                              backref='issue',
                              lazy=True
                              )
    created = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(), nullable=False)
    modified = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(),
                         onupdate=db.func.current_timestamp(), nullable=False)

    def __init__(self, name, description, issue_status_id, project_id, issue_type_id):
        self.name = name
        self.description = description
        self.issue_status_id = issue_status_id
        self.project_id = project_id
        self.issue_type_id = issue_type_id

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)

class IssueChangeLog(db.Model):
    """Data model for issue."""
    __tablename__ = "issue_change_log"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    field_name = db.Column(db.String(45),
                           unique=False,
                           nullable=False)

    old_value = db.Column(db.Text(),
                          unique=False,
                          nullable=False)

    new_value = db.Column(db.Text(),
                          unique=False,
                          nullable=False)

    issue_id = db.Column(db.Integer,
                         db.ForeignKey("issue.id"),
                         nullable=False)

    issue = db.relationship("Issue",
                            backref='issue_change_log',
                            lazy=True
                            )

    user_id = db.Column(db.Integer,
                        db.ForeignKey("user.id"),
                        nullable=False)

    user = db.relationship("User",
                           backref='issue_change_log',
                           lazy=True
                           )

    created = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(), nullable=False)
    modified = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(),
                         onupdate=db.func.current_timestamp(), nullable=False)

    def __init__(self, field_name=None, old_value=None, new_value=None, issue_id=None, user_id=None):
        self.field_name = field_name
        self.old_value = old_value
        self.new_value = new_value
        self.issue_id = issue_id
        self.user_id = user_id


class IssueStatus(db.Model):
    """Data model for role."""

    __tablename__ = "issue_status"
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    name = db.Column(db.String(45),
                     index=False,
                     unique=True,
                     nullable=False)

    issue = db.relationship(Issue,
                            backref='issue_status',
                            lazy=True)


class IssueType(db.Model):
    """Data model for role."""

    __tablename__ = "issue_type"
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    name = db.Column(db.String(45),
                     index=False,
                     unique=True,
                     nullable=False)

    issue = db.relationship(Issue,
                            backref='issue_type',
                            lazy=True)


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

    is_deleted = db.Column(db.Boolean,
                           default=False)

    created_by = db.Column(db.Integer,
                           db.ForeignKey("user.id"),
                           nullable=False)

    user = db.relationship("User",
                           lazy=True,
                           foreign_keys="Project.created_by")

    created = db.Column(db.DateTime(timezone=True),
                        default=db.func.current_timestamp(),
                        nullable=False)

    modified = db.Column(db.DateTime(timezone=True),
                         default=db.func.current_timestamp(),
                         onupdate=db.func.current_timestamp(),
                         nullable=False)

    def __init__(self, id=None, name=None, created_by=None):
        self.id = id
        self.name = name
        self.created_by = created_by


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


class UserProject(db.Model):
    """Data model for user project."""

    __tablename__ = "user_project"
    project_id = db.Column(db.Integer,
                           db.ForeignKey("project.id"),
                           primary_key=True)

    user_id = db.Column(db.Integer,
                        db.ForeignKey("user.id"),
                        primary_key=True)

    user = db.relationship("User",
                           lazy=True,
                           foreign_keys="UserProject.user_id")

    project = db.relationship("Project",
                              lazy=True,
                              foreign_keys="UserProject.project_id")

    def __init__(self, project_id, user_id):
        self.project_id = project_id
        self.user_id = user_id
