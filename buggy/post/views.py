from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import current_user

from .models import Post

blueprint = Blueprint('post', __name__, static_folder='../static')


@blueprint.route('/')
def posts():
    """Posts view"""
    posts = Post.query.all.order_by(Post.created_at)
    return render_template('posts/main.html', posts=posts)


@blueprint.route('/create_post/', methods=['GET', 'POST'])
def create_post():
    form = CreatePostForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            Post.create(
                title=form.title.data,
                content=form.content.data,
                user=current_user(),
            )
