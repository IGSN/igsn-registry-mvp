""" file:    test_api.py (tests)
    author: Jess Robertson, jessrobertson@icloud.com
    date:    July 2019

    description: Test base resources
"""

import json
import unittest
from itertools import product
from pathlib import Path

import ddt

from app import create_app
from app.config import config_by_name
from tests.utilities import APITestCase, TEST_RESOURCES

with open(TEST_RESOURCES / 'test_igsn_post_samples.json', 'r') as src:
    TEST_POST_DATA = json.load(src)

@ddt.ddt
class TestBaseResources(APITestCase):

    "Testing for API with mocked calls"

    @ddt.data('development', 'testing', 'production')
    def test_config(self, config_name):
        "Check config works ok"
        app = create_app(config_name)
        expected = config_by_name[config_name]().settings
        for key, value in expected.items():
            self.assertEqual(value, app.config[key])

    def test_blank_endpoint_fails(self):
        "Check the root endpoint 404s"
        self.request('/', expected_status=404, decode=False)

    def test_health_endpoint(self):
        "Check that the service is healthy"
        data, _ = self.request('/health')
        self.assertEqual(data['status'], 'success')
        self.assertTrue(len(data['results']) > 0)

    @ddt.data('application', 'config', 'os', 'python')
    def test_environment_endpoint_required_components(self, component):
        "Check the environment endpoint has required components"
        data, _ = self.request('/environment')
        self.assertIn(component, data.keys())

    @ddt.data('process', 'system')
    def test_environment_hidden_components(self, component):
        "Check the environment endpoint has hidden certain components"
        data, _ = self.request('/environment')
        self.assertNotIn(component, data.keys())

    def test_environment_check_config(self):
        "Check the config values are reported correctly"
        data, _ = self.request('/environment')

        # We need to ensure that any secret values are replaced by asterisks
        config = config_by_name['testing']()
        censor = lambda key, value: \
            '********' if any(s in key for s in ("KEY", "SECRET", "PASS")) else value
        expected = {k: censor(k, v) for k, v in config.settings.items()}

        # Check we get the right values
        for key, value in expected.items():
            self.assertEqual(value, data['config'][key])

    def test_sitemap(self):
        "Check the sitemap is available"
        data, _ = self.request('/sitemap')
        keys = set(k for k, _ in data)
        for key in ('/sitemap', '/environment', '/health'):
            self.assertIn(key, keys)

    # # todo are there restrictions on what an IGSN can be? e.g. ascii
    # @ddt.data(*TEST_POST_DATA)
    # @ddt.unpack
    # def test_hit_with_post(self, igsn, url, registrant):
    #     "Check we can post to the endpoint with the given method"
    #     # Test response
    #     postargs = {
    #         'url': url,
    #         'registrant': registrant
    #     }
    #     response = self.client.post(f'/igsn/{igsn}', data=postargs)
    #     data = get_json(response)
    #     self.assertTrue(data is not None)
    #     for key in ('message',):
    #         self.assertIn(key, data.keys())
    #         self.assertIn('Registered sample', data['message'])
    #         self.assertIn(igsn, data['message'])

    # @ddt.data('url', 'registrant')
    # def test_missing_argument(self, missing_arg):
    #     "Check a missing argument raises the right error"
    #     postargs = self.postargs
    #     del postargs[missing_arg]
    #     response = self.client.post(f'/igsn/{self.sampleNumber}', data=postargs)

    #     # Check we got a simple message
    #     data = get_json(response)
    #     self.assertTrue(data is not None)
    #     self.assertIn('message', data.keys())
    #     self.assertIn('errors', data.keys())
    #     self.assertTrue(isinstance(data['message'], str))
    #     self.assertIn(missing_arg, data['errors'].keys())

if __name__ == '__main__':
    unittest.main()
