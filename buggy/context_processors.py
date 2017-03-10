# -*- coding: utf-8 -*-
"""Context processors."""
from buggy.extensions import cache
from buggy.post.models import Tag


@cache.cached(timeout=60 * 30, key_prefix='all_tags')
def tags_processor():
    """15 most popular tags with posts reference counters."""
    tags = [(tag.name, len(tag.related_posts)) for tag in Tag.query.all()]
    tags.sort(key=lambda x: x[1], reverse=True)
    return dict(tags=tags[:15])
