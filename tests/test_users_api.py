""" file:    test_users_api.py (tests)
    author: Jess Robertson, jessrobertson@icloud.com
    date:    July 2019

    description: Test users resources
"""

import ddt

from app import create_app
from .utilities import APITestCase

@ddt.ddt
class TestBaseResources(APITestCase):

    def test_users_list(self):
        "Check we can hit the users endpoint"
        response = self.request('/users')
        self.assertEqual(response.json['meta']['count'], 0)
        self.assertEqual(response.json['data'], [])

    @ddt.data(*range(5))
    def test_users_by_id(self, ident):
        "Check we can get a user by ID"
        response = self.request(f'/users/{ident}')
        self.assertIsNone(response.json['data'])

    def test_role_list(self):
        "Check we can hit the roles endpoint"
        response = self.request('/roles')
        self.assertEqual(response.json['meta']['count'], 0)
        self.assertEqual(response.json['data'], [])

    @ddt.data(*range(5))
    def test_roles_by_id(self, ident):
        "Check we can get a role by ID"
        print(f'/roles/{ident}')
        response = self.request(f'/roles/{ident}')
        self.assertIsNone(response.json['data'])
