""" file:    config.py (igsn-registry-mvp)
    author:  Jess Robertson, jessrobertson@icloud.com
    date:    July 2019

    description: Flask configuration
"""

import os
from pathlib import Path

BASEDIR = Path(__file__).parent.parent.resolve()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'igsn-rocks-my-world')
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

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
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(BASEDIR / 'igsn_registry_dev.db')

class TestingConfig(Config):
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(BASEDIR / 'igsn_registry_test.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'path-to-postgres'

config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}