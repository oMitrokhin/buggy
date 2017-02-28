from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import login_user, login_required, logout_user

from buggy.utils import flash_errors

from .forms import LoginForm, RegisterForm
from .models import User

blueprint = Blueprint('user', __name__, static_folder='../static')


@blueprint.route('/login/', methods=['GET', 'POST'])
def login():
    """Login page"""
    form = LoginForm(request.form)
    # Handle logging in
    if request.method == 'POST':
        if form.validate_on_submit():
            login_user(form.user)
            flash('You are logged in.', 'success')
            redirect_url = request.args.get('next') or url_for('post.home')
            return redirect(redirect_url)
        else:
            flash_errors(form)
    return render_template('users/login.html', form=form)


@blueprint.route('/register/', methods=['GET', 'POST'])
def register():
    """Register page"""
    form = RegisterForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            User.create(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data,
                active=True
            )
            flash('You successfully registered. Please log in.', 'success')
            return redirect(url_for('user.login'))
        else:
            flash_errors(form)
    return render_template('users/register.html', form=form)


@blueprint.route('/logout/')
@login_required
def logout():
    """Logout."""
    logout_user()
    flash('You are logged out.', 'info')
    return redirect(url_for('post.home'))
