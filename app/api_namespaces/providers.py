""" file:    providers.py (igsn-registry-mvp)
    author:  Jess Robertson, jessrobertson@icloud.com
    date:    July 2019

    description: Provider resources
"""
# pylint: disable=C0103

from pathlib import Path
import logging

from flask import current_app
from flask_restplus import Resource, Namespace, reqparse

from .. import validate

namespace = Namespace('providers', description='IGSN provider information', path='/providers')

PROVIDER_DATA = [
    {
        "name": f"provider_{l}",
        "url": f"http://igsn.org/providers/provider_{l}"
    } for l in '12345'
]

@namespace.route('/')
class ProviderCollection(Resource):

    "Provider list endpoint"

    @namespace.doc('Get a list of the providers that IGSN knows about')
    def get(self):
        return PROVIDER_DATA
