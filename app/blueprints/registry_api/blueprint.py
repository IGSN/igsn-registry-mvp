""" file:    blueprint.py (igsn-registry-api)
    author:  Jess Robertson, jessrobertson@icloud.com
    date:    July 2019

    description: IGSN Registry API
"""
# pylint: disable=C0103

from flask import Blueprint
from flask_rest_jsonapi import Api

blueprint = Blueprint('igsn_registry_api', __name__)
api = Api(blueprint=blueprint)