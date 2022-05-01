"""Data models."""
from app import db


class User(db.Model):
    """Data model for user accounts."""

    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45), index=False, unique=True, nullable=False)
    password = db.Column(db.String(45), index=False, unique=True, nullable=False)

    def __repr__(self):
        return "<User {}>".format(self.username)
