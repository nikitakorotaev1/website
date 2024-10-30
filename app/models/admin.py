from flask_login import login_required

from ..extensions import db
from flask_admin import BaseView, expose, AdminIndexView
from .data import User


class AnyPageView(BaseView):
    @expose('/')
    @login_required
    def any_page(self):
        return self.render('admin/anypage/index.html')


class DashboardView(AdminIndexView):
    @expose('/')
    @login_required
    def add_data_db(self):

        all_users = User.query.all()


        return self.render('admin/dashboard.html', all_users=all_users)
