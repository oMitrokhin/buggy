# -*- coding: utf-8 -*-
"""Helper utilities and decorator"""
from functools import wraps

from flask import current_app, flash

from flask_login import current_user


class ValidationError(ValueError):
    """
    Raised when a validator fails to validate its input.
    """
    def __init__(self, message='', *args, **kwargs):
        ValueError.__init__(self, message, *args, **kwargs)


def flash_errors(form, category='warning'):
    """Flash all errors for a form"""
    for field, errors in form.errors.items():
        for error in errors:
            flash(
                '{0} - {1}'.format(getattr(form, field).label.text, error),
                category
            )


def get_or_create(cls, **kwargs):
    """Django cargo-cult."""
    instance = cls.query.filter_by(**kwargs).first()
    created = not instance
    res = cls.create(**kwargs) if created else instance
    return res, created


def length_validator(data, min, max):
    """
    Pass max = -1 to set up unlimited length.
    """
    l = data and len(data) or 0
    if l < min or max != -1 and l > max:
        if max == -1:
            message = 'Field must be at least %(min)d character long.'
            if min != 1:
                message.replace('character', 'characters')
        elif min == -1:
            message = 'Field cannot be longer than %(max)d character.'
            if max != 1:
                message.replace('character', 'characters')
        else:
            message = 'Field must be between %(min)d and' \
                      '%(max)d characters long.'
        raise ValidationError(message % dict(min=min, max=max, length=l))
    return data


def admin_user_required(func):
    """Decorates view to pass only admin users."""
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_app.login_manager._login_disabled:
            return func(*args, **kwargs)
        elif not current_user.is_admin:
            return current_app.login_manager.unauthorized()
        return func(*args, **kwargs)
    return decorated_view
