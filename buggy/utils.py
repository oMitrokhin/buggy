# -*- coding: utf-8 -*-
"""Helper utilities and decorator"""
from flask import flash


def flash_errors(form, category='warning'):
    """Flash all errors for a form"""
    for field, errors in form.errors.items():
        for error in errors:
            flash('{0} - {1}'.format(getattr(form, field).label.text, error), category)


def get_or_create(cls, **kwargs):
    instance = cls.query.filter_by(**kwargs).first()
    created = not instance
    res = cls.create(**kwargs) if created else instance
    return res, created
