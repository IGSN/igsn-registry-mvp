""" file:    utilities.py (tests)
    author:  Jess Robertson, jessrobertson@icloud.com
    date:    July 2019

    description: Common functionality for tests
"""

import json
from pathlib import Path
import unittest

from app import create_app

# Pointer to resources directory
TEST_RESOURCES = Path(__file__).parent / 'resources'

# A base class for testing JSON API reponses
class APITestCase(unittest.TestCase):

    """
    A class for testing our JSON API. Test cases should inherit from this

    Creates a `self.app` and `self.client` objects to manage the app instance and a client
    session for makinng requests.

    You should be able to do things like

    ```python
    response = self.request('/health')
    ```

    and have the JSON automatically decoded.
    """

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()

    def request(self, endpoint, method='get', expected_status=200, decode=True, *args, **kwargs):
        """
        Method for making requests against the API.

        Does a bunch of conversions and tests to ease ergonomics:
          - Check the return status is correct
          - Check we actually JSON in the response body
          - Covert Werkzeug response body to JSON.

        ..and then returns the JSON for further testing

        Parameters:
            method - the HTTP method to use (get, post, put, patch, delete)
            endpoint - the relative endpoint in the API to request from
            expected_status - the expected status. Optional, defaults to 200
            decode - if True, attempt to decode the JSON into a Python object. Optional,
                defaults to True. You probably want to set this to False if you're expecting
                a 4XX or similar.
            *args, **kwargs - get passed to underlying request call

        Returns:
            data, response - returns the JSON and the response class. If `decode=False` then
                the json object will be None.
        """
        # Make request
        try:
            response = getattr(self.client, method)(endpoint, *args, **kwargs)
        except AttributeError:
            self.fail("Unknown API method {}".format(method))

        # Check we got the right thing
        self.assertEqual(
            response.status_code, expected_status,
            'Unexpected status code {} from request to {}, expected {}.\nBody:{}'.format(
                response.status_code,
                endpoint,
                expected_status,
                response.get_data(as_text=True)))

        # If it's all good let's try to decode the response
        if decode:
            try:
                data = json.loads(response.get_data(as_text=True))
            except json.JSONDecodeError as err:
                self.fail('Recieved malformed JSON. Error was {}'.format(str(err)))
        else:
            data = None

        return data, response
