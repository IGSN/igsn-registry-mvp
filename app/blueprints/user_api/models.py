""" file:    models.py (igsn-user-api)
    author:  Jess Robertson, jessrobertson@icloud.com
    date:    July 2019

    description: Database models for SQLAlchemy for user blueprint
"""

from ...extensions.sqlalchemy import db, crypt

# Create the tables for our users in the database
class User(db.Model):

    """
    User model for storing user related details
    """

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    public_id = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(100))

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = crypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return crypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User '{}'>".format(self.username)

class Role(db.Model):

    "Role models for users"

    __tablename__ = "user_role"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True)