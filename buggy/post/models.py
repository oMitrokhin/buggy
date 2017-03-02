# -*- coding: utf-8 -*-
"""User models"""

import datetime as dt

from buggy.database import Column, Model, SurrogatePK, db, reference_col, relationship

tags_association_table = db.Table(
    'association',
    Model.metadata,
    Column('posts_id', db.Integer, db.ForeignKey('posts.id')),
    Column('tags_id', db.Integer, db.ForeignKey('tags.id'))
)


class Post(SurrogatePK, Model):
    """Posts model"""

    __tablename__ = 'posts'
    title = Column(db.String(200), nullable=False)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    content = Column(db.Text(), nullable=False)
    user_id = reference_col('users', nullable=True)
    user = relationship('User', backref='posts')
    related_tags = relationship(
        'Tag',
        secondary=tags_association_table,
        back_populates='related_posts',
    )

    def __init__(self, title, **kwargs):
        db.Model.__init__(self, title=title, **kwargs)

    def __repr__(self):
        return '<Post({title})>'.format(title=self.title)

    @property
    def cute_date(self):
        return self.created_at.strftime('Created %d, %b %Y')


class Tag(SurrogatePK, Model):
    """Tag model"""

    __tablename__ = 'tags'
    name = Column(db.String(100), nullable=False)
    related_posts = relationship(
        'Post',
        secondary=tags_association_table,
        back_populates='related_tags',
    )
