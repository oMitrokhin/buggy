# -*- coding: utf-8 -*-
"""User models"""
import datetime as dt

from flask_login import UserMixin

from buggy.database import (Column, Model, SurrogatePK, db, reference_col,
                            relationship)
from buggy.extensions import bcrypt


class Role(SurrogatePK, Model):
    """Role model."""
    __tablename__ = 'roles'
    name = Column(db.String(80), unique=True, nullable=False)
    user_id = reference_col('users', nullable=True)
    user = relationship('User', backref='roles')

    def __init__(self, name, **kwargs):
        """Forces to create instance with specific arguments."""
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Role({name})>'.format(name=self.name)


class User(UserMixin, SurrogatePK, Model):
    """User model."""
    __tablename__ = 'users'
    username = Column(db.String(80), unique=True, nullable=False)
    email = Column(db.String(80), unique=True, nullable=True)
    #: The hashed password
    password = Column(db.Binary(128), nullable=False)
    created_at = Column(
        db.DateTime, nullable=False, default=dt.datetime.utcnow
    )
    first_name = Column(db.String(30), nullable=True)
    last_name = Column(db.String(30), nullable=True)
    is_active = Column(db.Boolean(), default=False)
    is_admin = Column(db.Boolean(), default=False)

    def __init__(self, username, password, **kwargs):
        """Forces to create instance with specific arguments."""
        db.Model.__init__(self, username=username, password=password, **kwargs)
        self.set_password(password)

    def set_password(self, password):
        """
        Generate bcrypt hash of password string.
        """
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        """
        Verify that hash of value == hash of password.
        """
        return bcrypt.check_password_hash(self.password, value)

    @property
    def full_name(self):
        """Full name."""
        return '{0} {1}'.format(self.first_name, self.last_name)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<User({username!r})>'.format(username=self.username)
