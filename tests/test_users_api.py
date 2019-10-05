""" file:    test_users_api.py (tests)
    author: Jess Robertson, jessrobertson@icloud.com
    date:    July 2019

    description: Test users resources
"""

import ddt
from tests.utilities import APITestCase, TEST_RESOURCES

@ddt.ddt
class TestBaseResources(APITestCase):

    def test_users_list(self):
        "Check we can hit the users endpoint"
        # data, _ = self.request('/users')
        # self.assertEqual(data['meta']['count'], 0)
        # self.assertEqual(data['data'], [])
