""" file:    blueprint.py (igsn-user-api)
    author:  Jess Robertson, jessrobertson@icloud.com
    date:    July 2019

    description: IGSN API
"""
# pylint: disable=C0103

from flask import Blueprint
from flask_rest_jsonapi import Api

from .resources import UserList, UserDetail
from .models import *

blueprint = Blueprint('igsn_user_api', __name__)
api = Api(blueprint=blueprint)

# Users
api.route(UserList, 'user_list', '/users')
api.route(UserDetail, 'user_detail', '/users/<int:id>')