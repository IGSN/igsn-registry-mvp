""" file:   models.py (igsn-registry-api)
    author: Jess Robertson, jessrobertson@icloud.com
    date:   November 2019   
    description: Registry API database models
"""

import pendulum

from ...extensions.sqlalchemy import db

class Agent(db.Model):

    """
    Agent model - an IGSN agent which governs some namespace
    """

    __tablename__ = "agent"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    technical_contact = db.relationship('User')
    primary_contact = db.relationship('User')
    public_id = db.Column(db.String(255), unique=True, nullable=False)
    namespaces = db.relationship('Namespace', backref=db.backref('owner'))
    sitemaps = db.relationship('Sitemap', backref=db.backref('owner'))
    registered_on = db.Column(db.DateTime, default=pendulum.now())

    def __repr__(self):
        return f"<IGSN Agent '{self.public_id}'>"

class Namespace(db.Model):

    """
    Database representation for an IGSN namespace('
    """

    __tablename__ = "namespace"

    id = db.Column(db.Integer, primary_key=True)
    prefix = db.Column(db.String(255), unique=True, nullable=False)
    owner = db.relationship('Agent', backref=db.backref('namespaces'))
    in_sitemap = db.relationship('Sitemap', backref=db.backref('namespaces'))

    def __repr__(self):
        return f"<Namespace 'igsn.org/{self.prefix}'>"

class Sitemap(db.Model):

    """
    Sitemap representation
    """

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Unicode(1023), nullable=False)
    owner = db.relationship('Agent', backref=db.backref('sitemaps'))
    namespaces = db.relationship("Namespace")
    registered_on = db.Column(db.DateTime, default=pendulum.now)
    last_confirmed_on = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f"<Sitemap '{self.url}'>"
