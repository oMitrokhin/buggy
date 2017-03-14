# -*- coding: utf8 -*-
"""Post views module."""
from flask import (Blueprint, abort, flash, redirect, render_template, request,
                   url_for)
from flask_login import current_user, login_required
from sqlalchemy.orm import joinedload

from buggy.comment.forms import CreateCommentForm
from buggy.database import db
from buggy.settings import Config
from buggy.utils import admin_user_required, flash_errors, get_or_create

from .forms import CreatePostForm
from .models import Post, Tag

blueprint = Blueprint('posts', __name__, static_folder='../static')


@blueprint.route('/', defaults={'tag': None, 'page': 1})
@blueprint.route('/<page>', defaults={'tag': None})
@blueprint.route('/tag/<tag>', defaults={'page': 1})
@blueprint.route('/tag/<tag>/<page>')
def home(tag, page):
    """Posts view."""
    posts = Post.query.options(joinedload('related_tags')).order_by(
        Post.created_at.desc()
    )

    kwargs = {}
    if tag:
        posts = posts.filter(Post.related_tags.any(name=tag))
        # Paginator renderer uses url_for to generete paginator.
        # So we need somehow render urls with /tag/page
        kwargs['tag'] = tag

    paginator = posts.paginate(int(page), per_page=Config.POSTS_PER_PAGE)
    return render_template(
        'posts/home.html', posts=paginator.items, paginator=paginator,
        paginator_kwargs=kwargs
    )


@blueprint.route('/post/<slug>', methods=['GET'])
def post_detail(slug):
    """Post detail view."""
    form = CreateCommentForm(request.form)

    post = Post.query.options(
        joinedload('comments')
    ).filter_by(slug=slug).first()

    if not post:
        return abort(404)
    return render_template('posts/detail.html', post=post, form=form)


@blueprint.route('/create_post/', methods=['GET', 'POST'])
@login_required
@admin_user_required
def create_post():
    """Create post view."""
    form = CreatePostForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            post = Post.create(
                title=form.title.data,
                raw_content=form.content.data,
                user_id=current_user.id,
                slug=Post.make_slug(form.title.data)
            )

            # Create the TAGS!
            if form.tags.data:
                for tag in set(form.tags.data.split(', ')):
                    obj, _ = get_or_create(Tag, name=tag)
                    post.related_tags.append(obj)
                db.session.commit()

            flash('Post successfully added.', 'success')
            return redirect(url_for('posts.home'))
        else:
            flash_errors(form, 'danger')
    return render_template('posts/create_post.html', form=form)


@blueprint.route('/edit_post/<slug>', methods=['GET', 'POST'])
@login_required
@admin_user_required
def edit_post(slug):
    """Edit post view."""

    # Post must exist.
    post = Post.query.options(
        joinedload('related_tags')).filter_by(slug=slug).first()
    related_tags = post.related_tags
    if not post:
        abort(404)

    # Updating post on POST request.
    if request.method == 'POST':
        form = CreatePostForm(request.form)

        if form.validate_on_submit():
            form_tags = form.tags.data

            post.update(
                title=form.title.data,
                raw_content=form.content.data,
                user_id=current_user.id,
            )

            # Tags stuff
            old_tags = related_tags
            new_tags = set(form_tags.split(', ')) if form_tags else set()

            # Check if tags field changed.
            if new_tags != set(map(str, old_tags)):
                # Then performs tag create/delete operations.

                tags_to_create = new_tags - \
                                 set(tag for tag in set(map(str, old_tags)))
                tags_to_delete = [tag for tag in old_tags
                                  if str(tag) not in new_tags]

                # Search for new tags and create them if not exists.
                print(tags_to_create)
                for tag in tags_to_create:
                    obj, _ = get_or_create(Tag, name=tag)
                    post.related_tags.append(obj)

                # Remove not needed tags.
                for tag in tags_to_delete:
                    post.related_tags.remove(tag)

                db.session.commit()

            flash('Post {slug} was updated'.format(slug=post.slug), 'success')
        else:
            flash_errors(form, 'danger')
    else:
        # Render form with existing info.
        tags = ', '.join(str(tag) for tag in related_tags)

        form = CreatePostForm(obj=post)
        form.tags.data = tags

    # Finally, render form.
    return render_template(
        'posts/edit_post.html',
        form=form,
        post=post,
    )
