#!/usr/bin/env python
""" file:    run_api.py (igsn-registry-mvp)
    author:  Jess Robertson, jessrobertson@icloud.com
    date:    July 2019

    description: Run the API
"""
# pylint: disable=C0103,E1120

import click

from api import create_app

app = create_app()
app.app_context().push()

@click.command()
@click.option('-p', '--port', default='8080', help='The port to serve from')
@click.option('-h', '--host', default=None, help='The host IP')
@click.option('-d', '--debug', is_flag=True, help='Run in debug mode')
def run(host, port, debug):
    "Run the API"
    app.run(
        host=host,
        port=port,
        debug=debug)

if __name__ == '__main__':
    run()
