# -*- coding: utf-8 -*-
"""User models"""

import datetime as dt

from buggy.database import Column, Model, SurrogatePK, db, reference_col,\
    relationship

from slugify import UniqueSlugify


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
    content = Column(db.Text(), nullable=False)
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
        db.Model.__init__(self, title=title, **kwargs)

    def __repr__(self):
        return '<Post({title})>'.format(title=self.title)

    def save(self, commit=True):
        """
        Redefined to create unique post slug from title.
        """
        slugify_title = UniqueSlugify(
            unique_check=Post.unique_post_slug_checker,
            to_lower=True,
            max_length=50
        )
        self.slug = slugify_title(self.title)
        return super(Post, self).save(commit)

    @property
    def cute_date(self):
        """Date cutifier"""
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


class Tag(SurrogatePK, Model):
    """Post tags model"""

    __tablename__ = 'tags'
    name = Column(db.String(100), nullable=False)
    related_posts = relationship(
        'Post',
        secondary=tags_association_table,
        back_populates='related_tags',
    )
