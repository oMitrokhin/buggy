# -*- coding: utf-8 -*-
"""Useful database utilities and mixins"""

from .compat import basestring
from .extensions import db

# Alias common SQLAlchemy names
Column = db.Column
relationship = db.relationship


class CRUDMixin(object):
    """
    Mixin that adds convenience methods for
    CRUD (create, read, update, delete) operations.
    """

    @classmethod
    def create(cls, **kwargs):
        """
        Sugar
        """
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        """More sugar"""
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        """SUGAR"""
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        """...sugar"""
        db.session.delete(self)
        return commit and db.session.commit()


class Model(CRUDMixin, db.Model):
    """
    Base model class that includes CRUD convenience methods.
    """
    __abstract__ = True  # Tells alchemy not to create table in database


class SurrogatePK(object):
    """
    A mixin that adds surrogate primary key field 'id' to any
    declarative-mapped class.
    """

    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def get_by_id(cls, record_id):
        """
        Gets object by it's id.
        """
        if any(
                (isinstance(record_id, basestring) and record_id.isdigit(),
                 isinstance(record_id, (int, float)))
        ):
            return cls.query.get(int(record_id))
        return None


def reference_col(tablename, nullable=False, pk_name='id', **kwargs):
    """
    Stores references.
    """
    return db.Column(
        db.ForeignKey('{0}.{1}'.format(tablename, pk_name)),
        nullable=nullable, **kwargs
    )
