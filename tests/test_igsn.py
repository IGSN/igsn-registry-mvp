""" file:    test_igsn.py (tests)
    author: Jess Robertson, jessrobertson@icloud.com
    date:    July 2019

    description: Test IGSN resources
"""

import json
import unittest
from itertools import product
from pathlib import Path

import ddt

from app import create_app

def get_json(response):
    "Covert Werkzeug response body to JSON"
    return json.loads(response.get_data(as_text=True))

RESOURCES = Path(__file__).parent / 'resources'
with open(RESOURCES / 'test_igsn_post_samples.json', 'r') as src:
    TEST_POST_DATA = json.load(src)

@ddt.ddt
class TestIGSNResource(unittest.TestCase):

    "Testing for API with mocked calls"

    def setUp(self):
        self.app = create_app({
            'TESTING': True,
            'DEBUG': True
        })
        self.client = self.app.test_client()

        # Test data
        self.sampleNumber = 'foo1f32'
        self.postargs = {
            'url': '',
            'registrant': ' '
        }

    def test_config(self):
        "Check config works ok"
        self.assertFalse(create_app().testing)
        self.assertTrue(create_app({'TESTING': True}).testing)

    def test_endpoint_health(self):
        "Check we can get the endpoint"
        response = self.client.get('/igsn/')
        data = get_json(response)
        self.assertTrue(data is not None)
        self.assertIn('message', data.keys())
        self.assertTrue('up and running' in data['message'])

    @ddt.data('foo', 'bar', 'baz', 'quux', 'jess')
    def test_dummy_resolver(self, igsn):
        "Test our dummy resolver"
        response = self.client.get(f'/igsn/{igsn}')
        data = get_json(response)
        self.assertTrue(data is not None)
        self.assertIn('sampleNumber', data.keys())
        self.assertEqual(data['sampleNumber'], igsn)

    # todo are there restrictions on what an IGSN can be? e.g. ascii
    @ddt.data(*TEST_POST_DATA)
    @ddt.unpack
    def test_hit_with_post(self, igsn, url, registrant):
        "Check we can post to the endpoint with the given method"
        # Test response
        postargs = {
            'url': url,
            'registrant': registrant
        }
        response = self.client.post(f'/igsn/{igsn}', data=postargs)
        data = get_json(response)
        self.assertTrue(data is not None)
        for key in ('message',):
            self.assertIn(key, data.keys())
            self.assertIn('Registered sample', data['message'])
            self.assertIn(igsn, data['message'])

    @ddt.data('url', 'registrant')
    def test_missing_argument(self, missing_arg):
        "Check a missing argument raises the right error"
        postargs = self.postargs
        del postargs[missing_arg]
        response = self.client.post(f'/igsn/{self.sampleNumber}', data=postargs)

        # Check we got a simple message
        data = get_json(response)
        self.assertTrue(data is not None)
        self.assertIn('message', data.keys())
        self.assertIn('errors', data.keys())
        self.assertTrue(isinstance(data['message'], str))
        self.assertIn(missing_arg, data['errors'].keys())

if __name__ == '__main__':
    unittest.main()
