# -*- coding: utf8 -*-
"""Comment views."""
from flask import Blueprint, flash, redirect, request, url_for

from buggy.utils import flash_errors

from .forms import CreateCommentForm
from .models import Comment

blueprint = Blueprint('comments', __name__, static_folder='../static')


@blueprint.route('/post/<slug>/create_comment', methods=['POST'])
def create_comment(slug):
    form = CreateCommentForm(request.form)
    if form.validate_on_submit():
        Comment.create(
            name=form.name.data,
            email=form.email.data,
            text=form.text.data,
            post_id=int(form.post_id.data)
        )
        flash('Comment added.', 'success')
    else:
        flash_errors(form, 'danger')
    return redirect(url_for('posts.post_detail', slug=slug))
