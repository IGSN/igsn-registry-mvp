""" file:    models.py (igsn-user-api)
    author:  Jess Robertson, jessrobertson@icloud.com
    date:    July 2019

    description: Database models for SQLAlchemy for user blueprint. We define 
        a User who can belong to a Group (e.g. an Agent, or IGSN) and a set of 
        roles within that group (e.g. the technical contact, the primary contact,
        or a generic member)
"""

import pendulum
from sqlalchemy import Column, Table, Integer, ForeignKey, Unicode, DateTime, Boolean
from sqlalchemy.orm import relation

from ...extensions.sqlalchemy import db

# This is the assocation table for the many-to-many relationship between 
# groups and roles
group_role_assoc_table = Table(
    'group_to_role', db.Model.metadata,
    Column(
        'group_id', Integer, 
        ForeignKey('group.id', onupdate='CASCADE', ondelete='CASCADE'),
        primary_key=True),
    Column(
        'role_id', Integer, 
        ForeignKey('role.id', onupdate='CASCADE', ondelete='CASCADE'),
        primary_key=True)
)

# This is the association table for the many-to-many relationship between
# groups and members
user_group_assoc_table = Table(
    'user_to_group', db.Model.metadata,
    Column(
        'user_id', Integer, 
        ForeignKey('user.id', onupdate='CASCADE', ondelete='CASCADE'),
        primary_key=True),
    Column(
        'group_id', Integer, 
        ForeignKey('group.id', onupdate='CASCADE', ondelete='CASCADE'),
        primary_key=True)
)

# Create the tables for our users in the database
class User(db.Model):

    "User model for storing user related details"

    __tablename__ = "user"

    # Attributes
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(Unicode(255), unique=True, nullable=False)
    registered_on = Column(DateTime, default=pendulum.now)
    admin = Column(Boolean, nullable=False, default=False)
    public_id = Column(Unicode(255), unique=True)
    name = Column(Unicode(255), unique=True)

    # Relationships - roles and groups are included from association table relationships

    def __repr__(self):
        return "<User '{}'>".format(self.name)

class Group(db.Model):

    "Group model for storing IGSN user groups"

    __tablename__ = "group"

    # Attributes
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Unicode, unique=True, nullable=False)
    description = Column(Unicode(2047), nullable=True)

    # Relationships
    members = relation('User', secondary=user_group_assoc_table, backref='groups')

    def __repr__(self):
        return "<IGSN Group '{}'>".format(self.name)

class Role(db.Model):

    "Role models for users"

    __tablename__ = "role"

    # Attributes
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Unicode(255), unique=True)
    description = Column(Unicode(2047), nullable=True)

    # Relationships
    groups = relation('Group', secondary=group_role_assoc_table, backref='roles')

    def __repr__(self):
        return "<Role '{}'>".format(self.name)
