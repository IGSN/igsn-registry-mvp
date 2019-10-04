""" file:    user.py (igsn-registry-mvp/schemas)
    author:  Jess Robertson, jessrobertson@icloud.com
    date:    July 2019

    description: User schemas for serialization/validation
"""

from marshmallow_jsonapi.flask import Schema, Relationship
from marshmallow_jsonapi import fields

# Create a logical abstraction from the database for use in the API
class UserSchema(Schema):
    class Meta:
        type_ = 'user'
        self_view = 'models.user.user_detail'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'api.user_list'

    id = fields.Integer(as_string=True, dump_only=True)
    name = fields.Str(required=True, load_only=True)
    email = fields.Email(load_only=True)
    registered_on = fields.Date()
    display_name = fields.Function(lambda obj: "{} <{}>".format(obj.name.upper(), obj.email))

class UserRoleSchema(Schema):
    class Meta:
        type_ = 'user_role'
        self_view = 'models.user.user_role_detail'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'api.user_role_list'
