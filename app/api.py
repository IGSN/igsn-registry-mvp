""" file:    api.py (igsn-registry-mvp)
    author:  Jess Robertson, jessrobertson@icloud.com
    date:    July 2019

    description: IGSN API
"""
# pylint: disable=C0103

from flask import Blueprint
from flask_rest_jsonapi import Api

from .resources import user as user_resources

blueprint = Blueprint('api', __name__)
api = Api(blueprint=blueprint)

# Users
api.route(user_resources.UserList, 'user_list', '/users')
api.route(user_resources.UserDetail, 'user_detail', '/users/<int:id>')