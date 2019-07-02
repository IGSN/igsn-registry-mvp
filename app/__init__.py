""" file:    __init__.py (api)
    author:  Jess Robertson, jessrobertson@icloud.com
    date:    July 2019

    description: IGSN Registry API
"""

import logging

from flask import Flask, request
from flask.logging import default_handler
from flask_restplus import Api

from .api import blueprint as api_blueprint

# Add some extra info to flask logging
class RequestFormatter(logging.Formatter):
    "Add IP address etc to logging"
    def format(self, record):
        record.url = request.url
        record.remote_addr = request.remote_addr
        return super().format(record)

FORMATTER = RequestFormatter(
    '[%(asctime)s] %(remote_addr)s requested %(url)s\n'
    '%(levelname)s in %(module)s: %(message)s'
)
default_handler.setFormatter(FORMATTER)

def create_app(test_config=None):
    "Create and configure the Flask app serving our API"
    # Create & configure the app
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='igsn-rocks-my-world'
    )
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    app.logger.setLevel(logging.DEBUG)
    if app.config.get('DEBUG', False):
        app.logger.setLevel(logging.DEBUG)

    # Add the API resources
    app.register_blueprint(api_blueprint)

    # Return the configured app
    return app

def exception_handler(err, event, context):
    "Exception handler needed for lambda"
    print("ERROR {} {} {}".format(err, event, context))
    return True

if __name__ == '__main__':
    create_app({'DEBUG': True}).run(debug=True)
