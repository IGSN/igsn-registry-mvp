""" file:    factory.py (api)
    author:  Jess Robertson, jessrobertson@icloud.com
    date:    July 2019

    description: IGSN Registry app factory
"""

import logging

from flask import Flask, request
from flask.logging import default_handler
import pytest

# Now that resources are created we can import models/schemas etc
from .blueprints import user_api, registry_api, sitemap
from .config import config_by_name
from .extensions import db, migrate, health, envdump
from .errors import page_not_found, forbidden, server_error

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

# App factory
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
    app.logger.setLevel(logging.DEBUG)  # pylint: disable=E1101
    if app.config.get('DEBUG', False):
        app.logger.setLevel(logging.INFO)  # pylint: disable=E1101 
    
    # Add resources
    db.init_app(app)
    app.config['SQLALCHEMY_DB'] = db
    migrate.init_app(app, db)
    health.init_app(app, "/health")
    envdump.init_app(app, "/environment")

    # Add the API resources
    app.register_blueprint(user_api.blueprint)
    # app.register_blueprint(registry_api.blueprint)
    app.register_blueprint(sitemap.blueprint)

    # Add error handlers
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(403, forbidden)
    app.register_error_handler(500, server_error)

    # Add a testing command
    @app.cli.command('test')
    def test_app():  # pylint: disable=W0612
        pytest.main(['-s', 'tests'])

    # Return the configured app
    return app
