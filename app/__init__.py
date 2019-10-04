""" file:    __init__.py (api)
    author:  Jess Robertson, jessrobertson@icloud.com
    date:    July 2019

    description: IGSN Registry API
"""

import logging

from flask import Flask, request, Blueprint
from flask.logging import default_handler
from healthcheck import HealthCheck, EnvironmentDump
import pytest

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

# Now that resources are created we can import models/schemas etc
from .api import blueprint as api_blueprint
from .config import config_by_name
from .models.connections import db, crypt, migrate
from .health import health, envdump

def create_app(config=None):
    """
    Create and configure the Flask app serving our API

    Parameters:
        config - the name of an app configuration (see config.py for these)
            One of 'development', 'testing' or 'production'
    """
    # Create & configure the app
    app = Flask(__name__)
    try:
        app.config.from_object(config_by_name[config or 'development'])
    except KeyError:
        raise ValueError("Config must be one of 'development' or 'production'")

    # Configure logging
    app.logger.setLevel(logging.DEBUG)
    if app.config.get('DEBUG', False):
        app.logger.setLevel(logging.DEBUG)

    # Add the API resources
    app.register_blueprint(api_blueprint)

    # Add resources
    db.init_app(app)
    app.config['SQLALCHEMY_DB'] = db
    crypt.init_app(app)
    migrate.init_app(app, db)
    health.init_app(app, "/health")
    envdump.init_app(app, "/environment")

    # Add a testing command
    @app.cli.command('test')
    def test_app():
        pytest.main(['-s', 'tests'])

    # Return the configured app
    return app

def exception_handler(err, event, context):
    "Exception handler needed for lambda"
    print("ERROR {} {} {}".format(err, event, context))
    return True

if __name__ == '__main__':
    create_app({'DEBUG': True}).run(debug=True)
