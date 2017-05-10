# -*- coding: utf-8 -*-
from flask import Blueprint, render_template
from flask_login import login_required, current_user

from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView


class AdminView(BaseView):

    def is_accessible(self):
        return current_user.is_authenticated() and current_user.is_admin

# class ModelView(ModelView, AdminView):
#     pass

from ..extensions import flask_admin, db
from ..user.models import User
from ..public.models import Customer, Good, Container

flask_admin.add_view(ModelView(User, db.session, endpoint='user-admin'))
flask_admin.add_view(ModelView(Container, db.session, endpoint='container-admin'))
flask_admin.add_view(ModelView(Good, db.session, endpoint='good-admin'))
flask_admin.add_view(ModelView(Customer, db.session, endpoint='customer-admin'))
