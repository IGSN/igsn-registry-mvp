""" file:    sqlalchemy.py (igsn-registry-mvp.extensions)
    author:  Jess Robertson, jessrobertson@icloud.com
    date:    July 2019

    description: Healthcheck extensions for app
"""

from healthcheck import HealthCheck, EnvironmentDump
from flask import current_app
from sqlalchemy.orm import scoped_session

# Configure health checks
def sqlalchemy_available():
    "Check the SQLAlchemy engine is connected"
    try:
        db = current_app.config['SQLALCHEMY_DB']
        with db.engine.connect() as connection:
            connection.execute('SELECT 1;')
        return True, 'Database connection healthy'
    except Exception as err:
        return False, 'Database connection unhealthy: {}'.format(str(err))

health = HealthCheck()
health.add_check(sqlalchemy_available)

# Configure env dump
def application_data():
    return {
        "maintainer": "Jess Robertson",
        "git_repository": "https://github.com/igsn/igsn-registry-mvp.git"
    }

envdump = EnvironmentDump(include_process=False,)
envdump.add_section("application", application_data)