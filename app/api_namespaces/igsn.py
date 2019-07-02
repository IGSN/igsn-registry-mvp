""" file:    resolve.py (igsn-registry-mvp.api_namespaces)
    author:  Jess Robertson, jessrobertson@icloud.com
    date:    July 2019
    description: Demo resolver for when we don't want things to hook up to handle
"""
# pylint: disable=C0103

from pathlib import Path
import logging

from flask import current_app
from flask_restplus import Resource, Namespace, reqparse

from .. import validate

namespace = Namespace('igsn', description='IGSN registry/resolution', path='/igsn')

# Registration parsing
POST_PARSER = reqparse.RequestParser(bundle_errors=True)
POST_PARSER.add_argument(
    'url',
    required=True,
    location=('values', 'json', 'form')
)
POST_PARSER.add_argument(
    'registrant',
    required=True,
    location=('values', 'json', 'form')
)
POST_PARSER.add_argument(
    'relatedResourceIdentifier',
    required=False,
    location=('values', 'json', 'form')
)
POST_PARSER.add_argument(
    'log',
    required=False,
    location=('values', 'json', 'form')
)

@namespace.route('/')
class IGSNHealthCheck(Resource):

    "IGSN API Health check endpoint"

    @namespace.doc('Health check')
    def get(self):
        "Check the endpoint is up"
        current_app.logger.debug('Someone checking API health?')
        return {'message': 'IGSN Demo Resolver up and running!'}


# Todo: validate route using IGSN validator, with pluggable view, see http://flask.pocoo.org/docs/1.0/views/#views
@namespace.route('/<string:sampleNumber>')
class IGSN(Resource):

    def get(self, sampleNumber):
        "Resolve a sample"
        return {'sampleNumber': sampleNumber}

    @namespace.expect(POST_PARSER)
    def post(self, sampleNumber):
        "Register a sample"
        data = POST_PARSER.parse_args()
        current_app.logger.debug('Payload: %s', data)
        try:
            # Do the registration
            current_app.logger.info(f'Registering {sampleNumber}')
            return {'message': f'Registered sample {sampleNumber}'}

        except Exception as err:  # pylint: disable=W0703
            logging.exception('Hit exception, dumping debug info')
            return {"message": str(err)}, 422