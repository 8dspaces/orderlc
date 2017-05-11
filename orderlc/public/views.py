# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

from orderlc.extensions import login_manager
from orderlc.public.forms import LoginForm
from orderlc.user.forms import RegisterForm
from orderlc.user.models import User
from orderlc.utils import flash_errors

from .models import Good, Container, Customer

blueprint = Blueprint('public', __name__, static_folder='../static')


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))


@blueprint.route('/', methods=['GET', 'POST'])
def home():
    """Home page."""
    form = LoginForm(request.form)
    # Handle logging in
    if request.method == 'POST':
        if form.validate_on_submit():
            login_user(form.user)
            flash('You are logged in.', 'success')
            redirect_url = request.args.get('next') or url_for('user.members')
            return redirect(redirect_url)
        else:
            flash_errors(form)
    return render_template('public/home.html', form=form)


@blueprint.route('/logout/')
@login_required
def logout():
    """Logout."""
    logout_user()
    flash('You are logged out.', 'info')
    return redirect(url_for('public.home'))


@blueprint.route('/register/', methods=['GET', 'POST'])
def register():
    """Register new user."""
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        User.create(username=form.username.data, email=form.email.data, password=form.password.data, active=True)
        flash('Thank you for registering. You can now log in.', 'success')
        return redirect(url_for('public.home'))
    else:
        flash_errors(form)
    return render_template('public/register.html', form=form)


@blueprint.route('/about/')
def about():
    """About page."""
    form = LoginForm(request.form)
    return render_template('public/about.html', form=form)

@blueprint.route('/containers/')
def containers():
    containers = Container.query.all()
    return render_template('public/containers.html', containers=containers)



@blueprint.route('/goods/')
def goods():
    goods = []
    for g in Good.query.all():
        if g.get_location() == u'广州':
            goods.append(g)
    #prices = Good.query.filter(Good.get_location()=='广州').all()
    return render_template('public/goods.html',goods=goods  )

@blueprint.route('/prices/')
def prices():
    prices = Good.query.all()
    return render_template('public/prices.html',prices=prices )

@blueprint.route('/delivers/')
def delivers():
    delivers = []
    for g in Good.query.all():
        if g.get_location() == u'老挝':
            delivers.append(g)
    # delivers = Good.query.all().filter(Good.container.location=='老挝')
    return render_template('public/delivers.html', delivers=delivers)

@blueprint.route('/customers/')
def customers():
    customers = Customer.query.all()
    return render_template('public/customers.html', customers=customers)
