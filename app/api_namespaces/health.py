""" file:    health.py (igsn-registry-mvp.api_namespaces)
    author:  Jess Robertson, jessrobertson@icloud.com
    date:    July 2019
    description: Health-check endpoint
"""
# pylint: disable=C0103

from flask import current_app
from flask_restplus import Resource, Namespace, reqparse

namespace = Namespace('health', description='IGSN registry heartbeat', path='/health')

@namespace.route('/')
class IGSNHealthCheck(Resource):

    "IGSN API Health check endpoint"

    @namespace.doc('Health check')
    def get(self):
        "Check the endpoint is up"
        current_app.logger.debug('Someone checking API health?')
        return {'message': 'IGSN Registry up and running!'}
