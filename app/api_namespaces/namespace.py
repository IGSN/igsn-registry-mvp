""" file:    namespace.py (igsn-registry-mvp.api_namespaces)
    author:  Jess Robertson, jessrobertson@icloud.com
    date:    July 2019
    description: Demo namespace modelling
"""
# pylint: disable=C0103

from pathlib import Path
import logging

from flask import current_app
from flask_restplus import Resource, Namespace, reqparse

query_parser = reqparse.RequestParser()
query_parser.add_argument('name', required=False)

from .. import validate

namespace = Namespace('namespace', description='IGSN registry/resolution', path='/namespace')

# todo: replace with actual data
NAMESPACE_DATA = [
    {
        "name": f"namespace_{l}",
        "url": f"http://igsn.org/ns{l}"
    } for l in 'abcxyz'
]

@namespace.route('/')
class NamespaceCollection(Resource):

    "Namespace list endpoint"

    @namespace.doc('Get a list of the namespaces that IGSN knows about')
    @namespace.expect(query_parser)
    def get(self):
        args = query_parser.parse_args()
        current_app.logger.debug(args)
        if args['name']:
            for ns in NAMESPACE_DATA:
                if ns['name'] == args['name']:
                    return ns
            return {'message': "Couldn't find namespace {name}"}, 422
        else:
            return NAMESPACE_DATA

@namespace.route('/<string:namespace>')
class Namespace(Resource):

    "Namespace list endpoint"

    @namespace.doc('Get info about a particular namespace that IGSN knows about')
    def get(self, namespace):
        for ns in NAMESPACE_DATA:
            if ns['name'] == namespace:
                return ns
        return {'message': "Couldn't find namespace {name}"}, 422
