# -*- coding: utf-8 -*-
"""Context processors."""
from sqlalchemy.orm import joinedload

from buggy.extensions import cache
from buggy.post.models import Tag


@cache.cached(timeout=60 * 30, key_prefix='all_tags')
def tags_processor():
    """
    15 most popular tags with posts reference counters.
    Hides tags without any related posts.
    """
    tags = Tag.query.options(joinedload('related_posts')).all()
    top_tags = [(tag.name, len(tag.related_posts)) for tag in tags
                if tag.related_posts]
    top_tags.sort(key=lambda x: x[1], reverse=True)
    return dict(tags=top_tags[:15])
