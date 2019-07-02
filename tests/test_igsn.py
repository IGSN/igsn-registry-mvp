""" file:    test_api.py (tests)
    author: Jess Robertson, jess@unearthed.solutions
    date:    Thursday, 31 January 2019

    description: Test API factor
"""

import json
import unittest
from itertools import product

import ddt

from app import create_app

def get_json(response):
    "Covert Werkzeug response body to JSON"
    return json.loads(response.get_data(as_text=True))

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
            'url': 'https://igsn.org/foo1f32',
            'registrant': 'testing_framework'
        }

    def test_config(self):
        "Check config works ok"
        self.assertFalse(create_app().testing)
        self.assertTrue(create_app({'TESTING': True}).testing)

    def test_hit_with_get(self):
        "Check we can get the endpoint"
        response = self.client.get('/igsn/')
        data = get_json(response)
        self.assertTrue(data is not None)
        self.assertIn('message', data.keys())
        self.assertTrue('up and running' in data['message'])

    def test_hit_with_post(self):
        "Check we can get the endpoint with the given method"
        # Test response
        response = self.client.post(f'/igsn/{self.sampleNumber}', data=self.postargs)
        data = get_json(response)
        self.assertTrue(data is not None)
        for key in ('message',):
            self.assertIn(key, data.keys())

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
