""" file:    validators.py (igsn-registry-mvp)
    author:  Jess Robertson, jessrobertson@icloud.com
    date:    July 2019

    description: IGSN validators
"""

from flask import current_app

def string_to_igsn(string):
    "Validate that a string is a valid IGSN"
    # ascii
    # case insensitive
    return string.toascii().lower()

def string_to_registrant(string):
    "Check that a string is a valid registrant"
    current_app.logger.warn('Registrant validation not implemented yet!')
    return string