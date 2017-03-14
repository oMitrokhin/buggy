# -*- coding: utf-8 -*-
"""User models"""

import datetime as dt

from flask import Markup
from slugify import UniqueSlugify

from buggy.database import (Column, Model, SurrogatePK, db, reference_col,
                            relationship)

# ManyToMany stuff
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
    created_at = Column(
        db.DateTime, nullable=False, default=dt.datetime.utcnow
    )
    raw_content = Column(db.Text(), nullable=False)
    user_id = reference_col('users', nullable=True)
    user = relationship('User', backref='posts')
    related_tags = relationship(
        'Tag',
        secondary=tags_association_table,
        back_populates='related_posts',
    )
    slug = Column(
        db.String(50), nullable=True, unique=True
    )

    def __init__(self, title, **kwargs):
        """Forces to create instance with specific arguments."""
        db.Model.__init__(self, title=title, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Post({title})>'.format(title=self.title)

    @property
    def content(self):
        return Markup(self.raw_content)

    @property
    def cute_date(self):
        """Date cutifier."""
        return self.created_at.strftime('Created %d, %b %Y')

    @classmethod
    def unique_post_slug_checker(cls, text, uids):
        """
        Checks if slug already exists.
        Used in slugify.UniqueSlug from awesome-slugify.
        """
        if text in uids:
            return False
        return not Post.query.filter(Post.slug == text).first()

    @classmethod
    def make_slug(cls, title):
        """
        Redefined to create unique post slug from title.
        """
        slugify_title = UniqueSlugify(
            unique_check=Post.unique_post_slug_checker,
            to_lower=True,
            max_length=50
        )
        return slugify_title(title)


class Tag(SurrogatePK, Model):
    """Post tags model"""

    __tablename__ = 'tags'
    name = Column(db.String(100), nullable=False)
    related_posts = relationship(
        'Post',
        secondary=tags_association_table,
        back_populates='related_tags',
    )

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<Slug({name})>'.format(name=self.name)

    @classmethod
    def clean_unattached_tags(cls):
        """Cleans all tags, that are not attached to any post."""
        tags = cls.query.all()
        for tag in tags:
            if not tag.related_posts:
                tag.delete()
