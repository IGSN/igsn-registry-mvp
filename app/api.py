""" file:    api.py (igsn-registry-mvp)
    author:  Jess Robertson, jessrobertson@icloud.com
    date:    July 2019

    description: IGSN API
"""
# pylint: disable=C0103

from flask import Blueprint
from flask_restplus import Api

from .api_namespaces import igsn

blueprint = Blueprint('api', __name__)
api = Api(
    blueprint,
    title='IGSN Registry API MVP',
    version='1.0',
    description="An API for registring samples"
)

# api.add_namespace(providers)
# api.add_namespace(namespace)
api.add_namespace(igsn.namespace)
