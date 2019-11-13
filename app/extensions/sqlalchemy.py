""" file:    sqlalchemy.py (igsn-registry-mvp.extensions)
    author:  Jess Robertson, jessrobertson@icloud.com
    date:    July 2019

    description: SQLAlchemy extensions for app
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()