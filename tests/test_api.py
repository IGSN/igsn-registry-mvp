""" file:    test_api.py (tests)
    author: Jess Robertson, jessrobertson@icloud.com
    date:    July 2019

    description: Test base resources
"""

import json
from itertools import product
from pathlib import Path

import ddt

from app import create_app
from app.config import TestingConfig
from tests.utilities import APITestCase

@ddt.ddt
class TestBaseResources(APITestCase):

    "Testing for API with mocked calls"

    def test_config(self):
        "Check config works ok"
        expected = TestingConfig().settings
        for key, value in expected.items():
            self.assertEqual(value, self.app.config[key])

    def test_blank_endpoint_fails(self):
        "Check the root endpoint 404s"
        _ = self.request('/', status=404)

    def test_health_endpoint(self):
        "Check that the service is healthy"
        response = self.request('/health')
        self.assertEqual(response.json['status'], 'success')
        self.assertTrue(len(response.json['results']) > 0)

    @ddt.data('application', 'config', 'os', 'python')
    def test_environment_endpoint_required_components(self, component):
        "Check the environment endpoint has required components"
        response = self.request('/environment')
        self.assertIn(component, response.json.keys())

    @ddt.data('process', 'system')
    def test_environment_hidden_components(self, component):
        "Check the environment endpoint has hidden certain components"
        response = self.request('/environment')
        self.assertNotIn(component, response.json.keys())

    def test_environment_check_config(self):
        "Check the config values are reported correctly"
        response = self.request('/environment')

        # We need to ensure that any secret values are replaced by asterisks
        config = TestingConfig()
        censor = lambda key, value: \
            '********' if any(s in key for s in ("KEY", "SECRET", "PASS")) else value
        expected = {k: censor(k, v) for k, v in config.settings.items()}

        # Check we get the right values
        for key, value in expected.items():
            self.assertEqual(value, response.json['config'][key])

    def test_sitemap(self):
        "Check the sitemap is available"
        response = self.request('/sitemap')
        keys = set(k for k, _ in response.json)
        for key in ('/sitemap', '/environment', '/health'):
            self.assertIn(key, keys)
