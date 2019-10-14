""" file:    user.py (igsn-registry-mvp/schemas)
    author:  Jess Robertson, jessrobertson@icloud.com
    date:    July 2019

    description: User schemas for serialization/validation
"""

from marshmallow_jsonapi.flask import Schema, Relationship
from marshmallow_jsonapi import fields

# Create a logical abstraction from the database for use in the API
class User(Schema):
    class Meta:
        type_ = 'user'
        self_view = 'igsn_user_api.user_detail'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'igsn_user_api.user_list'

    id = fields.Integer(as_string=True, dump_only=True)
    username = fields.Str(required=True)
    email = fields.Email()
    registered_on = fields.Date()
    display_name = fields.Function(lambda obj: "{} <{}>".format(obj.name.upper(), obj.email))
    roles = Relationship(
        self_view='igsn_user_api.user_roles',
        self_view_kwargs={'id': '<id>'},
        related_view='igsn_user_api.role_list',
        related_view_kwargs={'id': '<id>'},
        many=True,
        schema='Role',
        type_='role',
        id_field='id'
    )

class Role(Schema):
    class Meta:
        type_ = 'role'
        self_view = 'igsn_user_api.role_detail'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'igsn_user_api.role_list'

    id = fields.Integer(as_string=True, dump_only=True)
    name = fields.Str(required=True, load_only=True)
    description = fields.Str(required=False)
    users = Relationship(
        attribute='user',
        self_view='user_deta'
    )
