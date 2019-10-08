""" file:    test_api.py (tests)
    author: Jess Robertson, jessrobertson@icloud.com
    date:    July 2019

    description: Test case utility for unit tests, lifted & lightly edited from flask-testing which
        doesn't seem to be maintained anymore. Note that we only care about the API tests here
        as I figure you'd use something else for testing the frontend.
"""

from unittest import TestCase
import gc
import logging
from pathlib import Path

from flask import json  # test with flask's JSON implementation
import flask_migrate
from werkzeug.utils import cached_property
import sqlalchemy

from app import create_app, db

MIGRATION_FOLDER = Path(__file__).parent.parent.resolve() / 'migrations'

## JSON Mixin class
# Just enables a response.json attribute similar to requests.Response.json
class JSONResponseMixin(object):
    "Enables a JSON object on a Werkzeug reponse"

    @cached_property
    def json(self):
        "Check and load JSON"
        try:
            return json.loads(self.data)
        except json.JSONDecodeError as err:
            raise ValueError(f'Recieved malformed JSON. Error was {str(err)}')

def add_json_property(response_class):
    "Add our JSON attribute to whatever response class we started with"
    class TestResponse(response_class, JSONResponseMixin):
        pass

    return TestResponse

class APITestCase(TestCase):

    environment = 'testing'  # don't set this to development or production unless you
                             # want to b0rk your database since we clean things out

    ## Setup and teardown hooks
    @classmethod
    def setUpClass(cls):
        # Migrate database
        app = create_app(cls.environment)
        with app.app_context():
            logging.debug('Running database migration')
            flask_migrate.upgrade()

    @classmethod
    def tearDownClass(cls):
        db.drop_all()
        db.engine.execute("DROP TABLE alembic_version")

    def setUp(self):
        # Construct app instance and client
        self.app = create_app(self.environment)
        self.orig_response = self.app.response_class
        self.app.response_class = add_json_property(self.app.response_class)

        # Create a client
        self.client = self.app.test_client()

    def tearDown(self):
        # Clean out database data from the session
        logging.debug('Removing test data')
        for table in reversed(db.metadata.sorted_tables):
            db.engine.execute(table.delete())
        db.session.commmit()
        db.session.remove()

    def request(self, endpoint, method='get', status=200, *args, **kwargs):
        """
        Make a request against the API endpoint, just does some added status checking
        """
        # Actually make request
        try:
            response = getattr(self.client, method)(endpoint, *args, **kwargs)
        except AttributeError:
            self.fail(f'Unknown API method {method}')

        # Check this went through ok
        self.assertStatus(response, status)
        return response

    # Broken out methods - todo add some common checks for each (e.g. is put/patch data updated?)
    def get(self, endpoint, status=200, *args, **kwargs):
        return self.request(endpoint, 'get', status, *args, **kwargs)

    def post(self, endpoint, status=200, *args, **kwargs):
        return self.request(endpoint, 'post', status, *args, **kwargs)

    def put(self, endpoint, status=200, *args, **kwargs):
        return self.request(endpoint, 'put', status, *args, **kwargs)

    def patch(self, endpoint, status=200, *args, **kwargs):
        return self.request(endpoint, 'patch', status, *args, **kwargs)

    def delete(self, endpoint, status=200, *args, **kwargs):
        return self.request(endpoint, 'delete', status, *args, **kwargs)

    def assertStatus(self, response, code, message=None):
        """
        Checks that a response status code is a given value

        Parameters:
            response - a Flask response
            code - the expected response status code (e.g. 200)
            message - the message to display on test failure
        """
        msg = message or f'Expected HTTP status {code} but got {response.status_code}'
        self.assertEqual(response.status_code, code, msg)
