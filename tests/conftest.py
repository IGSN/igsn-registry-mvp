""" file:    fixtures.py (tests)
    author: Jess Robertson, jessrobertson@icloud.com
    date:    July 2019

    description: Test case fixtures for unit tests using pytest. This is loaded directly using
        pytests fixture function discovery
"""

from pathlib import Path
import logging

import pytest
import flask_migrate
from werkzeug.utils import cached_property
import sqlalchemy

from app.factory import create_app
from app.extensions.sqlalchemy import db as _db

# Here we monkey-patch the Werkzeug response to add a Flask-enabled JSON response
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

## APP FIXTURES
@pytest.yield_fixture(scope='session')
def app(request):
    "Session-wide test `Flask` application"
    # Create the app and push the context prior to running tests
    app = create_app('testing')

    # Monkey-patch the Werkzeug responses with the JSON property
    _old_response_class = app.response_class
    app.response_class = add_json_property(app.response_class)

    # Push the context prior to running tests and kill on teardown
    ctx = app.app_context()
    ctx.push()

    yield app

    # Kill context on fixture teardown
    app.response_class = _old_response_class
    ctx.pop()

@pytest.fixture(scope='session')
def client(app, db, request):
    "Add an app client"
    return app.test_client()

## DATABASE FIXTURES
# Path to our alembic migrations
MIGRATION_FOLDER = Path(__file__).parent.parent.resolve() / 'migrations'

@pytest.yield_fixture(scope='session')
def db(app, request):
    "Session-wide test database"
    try:
        # Create database structure
        _db.app = app
        flask_migrate.upgrade(directory=str(MIGRATION_FOLDER))
        _db.create_all()

        yield _db

    # Unload tables on fixture teardown
    finally:
        # ensure that all sessions have closed or the connection will hang!
        sqlalchemy.orm.session.close_all_sessions()

        # Clear out database
        _db.reflect()
        _db.drop_all()

## SESSION FIXTURE
@pytest.yield_fixture(scope='function')
def db_session(db, request):
    "Creates a new database session for a test"
    # Every session runs inside a transaction
    connection = db.engine.connect()
    transaction = connection.begin()
    options = {'bind': connection, 'binds': {}}
    session = db.create_scoped_session(options=options)
    db.session = session

    yield session

    # Roll back the transaction on teardown
    transaction.rollback()
    connection.close()
    session.remove()
