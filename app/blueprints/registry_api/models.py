""" file:   models.py (igsn-registry-api)
    author: Jess Robertson, jessrobertson@icloud.com
    date:   November 2019   
    description: Registry API database models
"""

import pendulum
from sqlalchemy import Column, Table, Integer, DateTime, Boolean, Unicode, ForeignKey
from sqlalchemy.orm import relationship

from ...extensions.sqlalchemy import db

class Agent(db.Model):

    """
    Agent model - an IGSN agent which governs some namespace
    """

    __tablename__ = "agent"

    # Attributes
    id = Column(Integer, primary_key=True)
    technical_contact_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    primary_contact_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    public_id = Column(Unicode(255), unique=True, nullable=False)
    registered_on = Column(DateTime, default=pendulum.now())

    # Relationships
    technical_contact = relationship('User', foreign_keys='Agent.technical_contact_id', uselist=False)
    primary_contact = relationship('User', foreign_keys='Agent.primary_contact_id', uselist=False)
    namespaces = relationship('Namespace', back_populates='owner')
    sitemaps = relationship('Sitemap', back_populates='owner')

    def __repr__(self):
        return f"<IGSN Agent '{self.public_id}'>"

class Namespace(db.Model):

    """
    Database representation for an IGSN namespace('
    """

    __tablename__ = "namespace"

    # Attributes
    id = Column(Integer, primary_key=True, autoincrement=True)
    prefix = Column(Unicode(255), unique=True, nullable=False)
    owner_id = Column(Integer, ForeignKey('agent.id'))
    sitemap_id = Column(Integer, ForeignKey('sitemap.id'))

    # Relationships
    owner = relationship('Agent', foreign_keys='Namespace.owner_id', 
                         back_populates='namespaces', uselist=False)
    sitemap = relationship('Sitemap', foreign_keys='Namespace.sitemap_id', 
                           back_populates='namespaces', uselist=False)

    def __repr__(self):
        return f"<Namespace 'igsn.org/{self.prefix}'>"

class Sitemap(db.Model):

    """
    Sitemap representation
    """
    
    # Attributes
    id = Column(Integer, primary_key=True)
    url = Column(Unicode(1023), nullable=False)
    owner_id = Column(Integer, ForeignKey('agent.id'), primary_key=True)
    registered_on = Column(DateTime, default=pendulum.now)
    last_confirmed_on = Column(DateTime, nullable=True)

    # Relationships
    owner = relationship('Agent', back_populates='sitemaps')
    namespaces = relationship("Namespace", back_populates='sitemap')

    def __repr__(self):
        return f"<Sitemap '{self.url}'>"
