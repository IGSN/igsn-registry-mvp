""" file:    config.py (igsn-registry-mvp)
    author:  Jess Robertson, jessrobertson@icloud.com
    date:    July 2019

    description: Flask configuration
"""

import os
from pathlib import Path

def generate_db_uri(host, name, port=None, user=None, engine=None):
    "Dynamically load a SQLAlchemy URI generated from other options"
    try:
        db_engine = engine or os.environ['FLASK_DB_ENGINE']
    except KeyError:  # fall back to SQLite as default
        db_engine = 'sqlite'

    # Load up database string
    if db_engine in {'postgresql', 'postgres'}:
        if user is not None and user != '':
            host = f'{user}@{host}'
        if port is not None and port != '':
            host = f'{host}:{port}'
        return f'postgresql://{host}/{name}'

    elif db_engine == 'sqlite':
        basedir = Path(__file__).parent.parent.resolve()
        return 'sqlite:///' + str(basedir / f'{name}.db')

    else:
        raise ValueError(f'Unknown database engine {engine}')

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'igsn-rocks-my-world')
    DEBUG = False
    TESTING = False

    # Database options
    DB_ENGINE = os.getenv('FLASK_DB_ENGINE', 'sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False

    # Pagination options
    PAGE_SIZE = 30

    @property
    def settings(self):
        "Convert config class to a settings dictionary"
        return {
            key: getattr(self, key) for key in dir(self)
            if not key.startswith('__')
            and key != 'settings'
            and not callable(getattr(self, key))
        }

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = generate_db_uri(
        engine=os.environ.get('FLASK_DEV_DB_ENGINE', None),
        user=os.environ.get('FLASK_DEV_DB_USER', None),
        host=os.environ.get('FLASK_DEV_DB_HOST', None),
        port=os.environ.get('FLASK_DEV_DB_PORT', None),
        name=os.environ.get('FLASK_DEV_DB_NAME', None)
    )

class TestingConfig(Config):
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = generate_db_uri(
        engine=os.environ.get('FLASK_TEST_DB_ENGINE', None),
        user=os.environ.get('FLASK_TEST_DB_USER', None),
        host=os.environ.get('FLASK_TEST_DB_HOST', None),
        port=os.environ.get('FLASK_TEST_DB_PORT', None),
        name=os.environ.get('FLASK_TEST_DB_NAME', None)
    )

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = generate_db_uri(
        engine=os.environ.get('FLASK_DB_ENGINE', None),
        user=os.environ.get('FLASK_DB_USER', None),
        host=os.environ.get('FLASK_DB_HOST', None),
        port=os.environ.get('FLASK_DB_PORT', None),
        name=os.environ.get('FLASK_DB_NAME', None)
    )

config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}