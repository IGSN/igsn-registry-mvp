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

# Construct some accounts for testing
@pytest.fixture(scope='session')
def users(db, n_users=2):
    """
    Create fake users for the app.

    Creates a list of an admin account (`users[0]`) and 10 normal users (`users[1:]`)
    and commits all these to the database
    """
    users = [AdminFactory.build()] + list(UserFactory.build_batch(n_users))
    db.session.add_all(users)
    db.session.commit()
    return users

# Test suite
def test_add_users(users):
    "Check we have created the users ok"
    for user in users:
        assert user.id is not None
        assert user.check_password('sup3rs3cr3t')
        with pytest.raises(AttributeError):
            user.password

def test_add_admin(users):
    "Check we've added the admin account"
    admin = users[0]
    assert admin.id is not None
    assert admin.check_password('sup3rs3cr3t')

def test_users_list(client, users):
    "Check that we can hit the users endpoint"
    try:
        response = client.get('/users')
        assert response.status_code == 200
    except AssertionError:
        print(response)
    assert response.json['meta']['count'] == len(users)
    assert response.json['data'] != []

def test_users_detail(client, users):
    "Check the user detail view by id"
    for user in users:
        response = client.get(f'/users/{user.id}')
        assert response.status_code == 200

        # Check response
        data = response.json['data']
        assert data['type'] == 'user'
        assert data['links']['self'] == f'/users/{user.id}'
        expected = {'username': user.username, 'email': user.email}
        for key, expected_value in expected.items():
            assert data['attributes'][key] == expected_value

def test_users_simple_filter(client, users):
    "Check the user detail view by id"
    for user in users:
        response = client.get(f'/users?filter[username]={user.username}')
        assert response.status_code == 200
        assert response.json['data'][0]['links']['self'] == f'/users/{user.id}'
