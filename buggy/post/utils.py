# -*- coding: utf-8 -*-
"""Post app utils."""
from .models import Tag


def tags_by_data(data):
    """
    By single request to DB returns all tags that must be attached to post.
    """
    input_tags = set(map(str.strip, data.split(',')))
    input_tags.discard('')

    existing_tags = Tag.query.filter(Tag.name.in_(input_tags))

    new_tags = input_tags - set(map(str, existing_tags))

    # Return just created and already existed tags.
    return [Tag(name=tag) for tag in new_tags] + list(existing_tags)
