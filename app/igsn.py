""" file:    igsn.py (igsn-registry-mvp)
    author:  Jess Robertson, jessrobertson@icloud.com
    date:    July 2019

    description: IGSN namespace
"""
# pylint: disable=C0103

from pathlib import Path
import logging

from flask import current_app
from flask_restplus import Resource, Namespace, reqparse

from . import validate

LOGGER = logging.getLogger('explore-australia-lambda')

api = Namespace('scoring', description='Scoring', path='/')

POST_PARSER = reqparse.RequestParser(bundle_errors=True)
POST_PARSER.add_argument(
    'sampleNumber',
    required=True,
    location=('values', 'json', 'form'),
    type=validate.string_to_igsn
)
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

@api.route('/igsn')
class IGSNCollection(Resource):

    "IGSN Collection API"

    @api.doc('Health check')
    def get(self):
        "Check the endpoint is up"
        current_app.logger.debug('Someone checking API health?')
        return {'message': 'IGSN Registry API up and running!'}


# Todo: validate route using IGSN validator, with pluggable view, see http://flask.pocoo.org/docs/1.0/views/#views
@api.route('/igsn/<string:sampleNumber>')
class IGSN(Resource)

    def get(self, sampleNumber):
        return {'sample': sampleNumber}

    @api.expect(POST_PARSER)
    def post(self, sampleNumber):
        "Score a submission"
        data = POST_PARSER.parse_args()
        current_app.logger.debug('Payload: %s', data)
        try:
            # Do the registration
            current_app.logger.info(f'Registering {data['sampleNumber']}')
            return {'message': f'Registered sample {data['sampleNumber']}'}

        except Exception as err:  # pylint: disable=W0703
            logging.exception('Hit exception, dumping debug info')
            return {"message": str(err)}, 422

