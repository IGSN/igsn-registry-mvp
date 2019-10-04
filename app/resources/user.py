""" file:    user.py (igsn-registry-mvp/resources)
    author:  Jess Robertson, jessrobertson@icloud.com
    date:    July 2019

    description: User resources for JSON API
"""


from flask_rest_jsonapi import ResourceList, ResourceRelationship, ResourceDetail

from ..schemas.user import UserSchema, UserRoleSchema
from ..models.user import User, UserRole
from ..models.connections import db

# Create resource managers
class UserDetail(ResourceDetail):

    def before_get_object(self, view_kwargs):
        "Materialize role details on view"
        if view_kwargs.get('role_id') is not None:
            try:
                role = self.session.query(Role).filter_by(id=view_kwargs['role_id']).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {'parameter': 'role_id'},
                    'Role with id {} not found'.format(view_kwargs['role_id'])
                )

    schema = UserSchema
    data_layer = {
        "session": db.session,
        "model": User,
        "methods": {'before_get_object': before_get_object}
    }

class UserList(ResourceList):
    schema = UserSchema
    data_layer = {
        'session': db.session,
        'model': User
    }

class UserRoleList(ResourceList):
    schema = UserRoleSchema
    data_layer = {
        'session': db.session,
        'model': UserRole
    }