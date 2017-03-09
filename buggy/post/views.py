# -*- coding: utf8 -*-
from flask import Blueprint, render_template, request, redirect, flash,\
    url_for, abort
from flask_login import current_user, login_required
from sqlalchemy.orm import joinedload

from buggy.utils import flash_errors, get_or_create
from buggy.database import db
from buggy.extensions import cache
from buggy.comment.forms import CreateCommentForm

from .forms import CreatePostForm
from .models import Post, Tag

blueprint = Blueprint('posts', __name__, static_folder='../static')


@blueprint.route('/', defaults={'tag': None})
@blueprint.route('/tag/<tag>')
@cache.cached(timeout=50)
def home(tag):
    """Posts view"""
    posts = Post.query.options(joinedload('related_tags')).order_by(
        Post.created_at.desc()
    )
    if tag:
        posts = posts.filter(Post.related_tags.any(name=tag))
    return render_template('posts/home.html', posts=posts)


@blueprint.route('/post/<slug>', methods=['GET'])
@cache.cached(timeout=10)
def post_detail(slug):
    form = CreateCommentForm(request.form)

    post = Post.query.options(
        joinedload('comments')
    ).filter_by(slug=slug).first()

    if not post:
        return abort(404)
    return render_template('posts/detail.html', post=post, form=form)


@blueprint.route('/create_post/', methods=['GET', 'POST'])
@login_required
def create_post():
    """Create post view"""
    form = CreatePostForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            post = Post.create(
                title=form.title.data,
                content=form.content.data,
                user_id=current_user.id,
            )
            for tag in form.tags.data.split(', '):
                print(tag)
                obj, _ = get_or_create(Tag, name=tag)
                post.related_tags.append(obj)
            db.session.commit()
            flash('Post successfully added.', 'success')
            return redirect(url_for('posts.home'))
        else:
            flash_errors(form, 'danger')
    return render_template('posts/create_post.html', form=form)
