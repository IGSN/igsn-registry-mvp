""" file:    resources.py (igsn-user-api)
    author:  Jess Robertson, jessrobertson@icloud.com
    date:    July 2019

    description: JSON API resources for IGSN user blueprint
"""

from flask_rest_jsonapi import ResourceList, ResourceRelationship, ResourceDetail
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound

from ...extensions.sqlalchemy import db
from . import models, schemas

class UserDetail(ResourceDetail):
    "User detail JSON API resource"

    def before_get_object(self, view_kwargs):
        "Materialize role details on view"
        if view_kwargs.get('role_id') is not None:
            try:
                role = self.session.query(models.Role).filter_by(id=view_kwargs['role_id']).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {'parameter': 'role_id'},
                    'Role with id {} not found'.format(view_kwargs['role_id'])
                )

    schema = schemas.User
    data_layer = {
        "session": db.session,
        "model": models.User,
        "methods": {'before_get_object': before_get_object}
    }

class UserList(ResourceList):
    "User list JSON API resource"
    schema = schemas.User
    data_layer = {
        'session': db.session,
        'model': models.User
    }

class RoleDetail(ResourceDetail):
    "Role detail JSON API resource"

    def before_get_object(self, view_kwargs):
        "Materialize role details on view"
        if view_kwargs.get('role_id') is not None:
            try:
                users = self.session.query(models.User).filter_by(id=view_kwargs['user_id']).all()
            except NoResultFound:
                raise ObjectNotFound(
                    {'parameter': 'user_id'},
                    'User with id {} not found'.format(view_kwargs['user_id'])
                )

    schema = schemas.User
    data_layer = {
        "session": db.session,
        "model": models.Role,
        "methods": {'before_get_object': before_get_object}
    }

class RoleList(ResourceList):
    "Role list JSON API resource"
    schema = schemas.Role
    data_layer = {
        'session': db.session,
        'model': models.Role
    }
