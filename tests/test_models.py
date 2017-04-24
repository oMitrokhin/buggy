# -*- coding: utf-8 -*-
"""Model unit tests."""
import datetime as dt

import pytest

from buggy.user.models import Role, User

from .factories import UserFactory


@pytest.mark.usefixtures('db')
class TestUser:
    """User tests."""

    def test_get_by_id(self):
        """Get user by ID."""
        user = User('foo', 'foo@bar.com')
        user.save()

        retrieved = User.get_by_id(user.id)
        assert retrieved == user

    def test_created_at_defaults_to_datetime(self):
        """Test creation date."""
        user = User(username='foo', email='foo@bar.com', password='testpass')
        user.save()
        assert bool(user.created_at)
        assert isinstance(user.created_at, dt.datetime)

    def test_password_not_nullable(self):
        """Test null password."""
        with pytest.raises(TypeError):
            User(username='foo', email='foo@bar.com')

    def test_factory(self, db):
        """Test user factory."""
        user = UserFactory()
        db.session.commit()
        assert bool(user.username)
        assert bool(user.email)
        assert bool(user.created_at)
        assert user.is_admin is False
        assert user.is_active is True
        assert user.check_password('myPasswd123')

    def test_check_password(self):
        """Check password."""
        user = User.create(username='foo', email='foo@bar.com',
                           password='foobarbaz123')
        assert user.check_password('foobarbaz123') is True
        assert user.check_password('barfoobaz') is False

    def test_full_name(self):
        """User full name."""
        user = UserFactory(
            first_name='Foo',
            last_name='Bar',
            password='myprecious'
        )
        assert user.full_name == 'Foo Bar'

    def test_roles(self):
        """Add a role to a user."""
        role = Role(name='admin')
        role.save()
        user = UserFactory()
        user.roles.append(role)
        user.save()
        assert role in user.roles
