""" file:   errors.py
    author: Jess Robertson

    description: Error handlers
"""

from flask import jsonify

def page_not_found(err):
    "HTTP404 error handler"
    return jsonify(error=str(err)), 404

def forbidden(err):
    "HTTP403 error handler"
    return jsonify(error=str(err)), 403

def server_error(err):
    "HTTP500 error handler"
    return jsonify(error=str(err)), 500
