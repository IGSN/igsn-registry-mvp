""" file:    test_api.py (tests)
    author: Jess Robertson, jessrobertson@icloud.com
    date:    July 2019

    description: Test base resources
"""

import json
from itertools import product
from pathlib import Path

import pytest

from app.config import TestingConfig

def test_config(app):
    "Check config works ok"
    expected = TestingConfig().settings
    for key, value in expected.items():
        assert value == app.config[key]

def test_blank_endpoint_fails(client):
    "Check the root endpoint 404s"
    response = client.get('/')
    assert response.status_code == 404

def test_health_endpoint(client):
    "Check that the service is healthy"
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json['status'] == 'success'
    assert len(response.json['results']) > 0

@pytest.mark.parametrize('component', ['application', 'config', 'os', 'python'])
def test_environment_endpoint_required_components(client, component):
    "Check the environment endpoint has required components"
    response = client.get('/environment')
    assert response.status_code == 200
    assert component in response.json.keys()

@pytest.mark.parametrize('component', ['process', 'system'])
def test_environment_hidden_components(client, component):
    "Check the environment endpoint has hidden certain components"
    response = client.get('/environment')
    assert response.status_code == 200
    assert component not in response.json.keys()

def test_environment_check_config(client):
    "Check the config values are reported correctly"
    response = client.get('/environment')
    assert response.status_code == 200

    # We need to ensure that any secret values are replaced by asterisks
    config = TestingConfig()
    censor = lambda key, value: \
        '********' if any(s in key for s in ("KEY", "SECRET", "PASS")) else value
    expected = {k: censor(k, v) for k, v in config.settings.items()}

    # Check we get the right values
    for key, value in expected.items():
        assert value == response.json['config'][key]

def test_sitemap(client):
    "Check the sitemap is available"
    response = client.get('/sitemap')
    assert response.status_code == 200
    keys = set(k for k, _ in response.json)
    for key in ('/sitemap', '/environment', '/health'):
        assert key in keys
