""" file:    test_users_api.py (tests)
    author: Jess Robertson, jessrobertson@icloud.com
    date:    July 2019

    description: Test users resources
"""

import pytest
import factory
from factory.alchemy import SQLAlchemyModelFactory as Factory

from app.factory import create_app
from app.blueprints.user_api import models

# FactoryBoy factories for users
class AdminFactory(Factory):
    class Meta:
        model = models.User

    admin = True
    email = 'admin@igsn.org'
    password = 'sup3rs3cr3t'
    public_id = 'Adam McAdminface'
    registered_on = factory.Faker('date_time_between', start_date="-30y", end_date="now")
    username='admin'

class UserFactory(Factory):
    class Meta:
        model = models.User

    admin = False
    email = factory.LazyAttribute(lambda a: a.public_id.lower().replace(' ', '.') + '@example.com')
    password = 'sup3rs3cr3t'
    public_id = factory.Faker('name')
    registered_on = factory.Faker('date_time_between', start_date="-30y", end_date="now")
    username=factory.LazyAttribute(lambda a: a.public_id.lower().replace(' ', '_'))

@pytest.mark.parametrize('user', UserFactory.build_batch(7))
def test_add_user(db_session, user):
    db_session.add(user)
    db_session.commit()
    assert user.id > 0
    assert user.check_password('sup3rs3cr3t')

def test_add_admin(db_session, foo=5):
    admin = AdminFactory.build()
    db_session.add(admin)
    db_session.commit()
    assert admin.id > 0
    assert admin.check_password('sup3rs3cr3t')
    with pytest.raises(AttributeError):
        admin.password

# from .utilities import APITestCase

# @ddt.ddt
# class TestBaseResources(APITestCase):

#     def test_users_list(self):
#         "Check we can hit the users endpoint"
#         response = self.request('/users')
#         self.assertEqual(response.json['meta']['count'], 0)
#         self.assertEqual(response.json['data'], [])

#     @ddt.data(*range(5))
#     def test_users_by_id(self, ident):
#         "Check we can get a user by ID"
#         response = self.request(f'/users/{ident}')
#         self.assertIsNone(response.json['data'])

#     def test_role_list(self):
#         "Check we can hit the roles endpoint"
#         response = self.request('/roles')
#         self.assertEqual(response.json['meta']['count'], 0)
#         self.assertEqual(response.json['data'], [])

#     @ddt.data(*range(5))
#     def test_roles_by_id(self, ident):
#         "Check we can get a role by ID"
#         print(f'/roles/{ident}')
#         response = self.request(f'/roles/{ident}')
#         self.assertIsNone(response.json['data'])
