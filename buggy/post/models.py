# -*- coding: utf-8 -*-
"""User models"""

import datetime as dt

from buggy.database import Column, Model, SurrogatePK, db, reference_col, relationship


class Post(SurrogatePK, Model):
    """Posts model"""

    __tablename__ = 'posts'
    title = Column(db.String(200), nullable=False)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    content = Column(db.Text(), nullable=False)
    user_id = reference_col('users', nullable=True)
    user = relationship('User', backref='posts')

    def __init__(self, title, **kwargs):
        db.Model.__init__(title=title, **kwargs)

    def __repr__(self):
        return '<Post({title})>'.format(title=self.title)
