from flask import Flask
from flask_admin.theme import BootstrapTheme, Bootstrap4Theme
from flask_login import login_required

from .extensions import login_manager
from .routes.user import user_routes
from .extensions import db, migrate
from .config import Config

# from .routes.user import user
from .routes.post import post
from .models.data import *
from .models.admin import *
from .models.post import Post

from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # app.register_blueprint(user)
    app.register_blueprint(post)
    app.register_blueprint(user_routes)


    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    #Login Manager
    login_manager.login_view = 'user_routes.login'
    login_manager.login_message = 'Требуется авторизация'
    login_manager.login_message_category = 'info'


   # Создание панели управления через flask-admin
    admin = Admin(app, name='Панель Управления', index_view=DashboardView(), endpoint='admin')

    admin.add_view(RoleView(Role, db.session, name='Роль'))
    admin.add_view(UserView(User, db.session, name='Пользователи'))
    admin.add_view(PersonnelView(Personnel, db.session, name='Персонал'))
    admin.add_view(DepartmentView(Department, db.session, name='Отделы'))
    admin.add_view(ProjectView(Project, db.session, name='Проекты'))
    admin.add_view(FinanceView(Finance, db.session, name='Финансы'))
    admin.add_view(ClientOrderView(ClientOrder, db.session, name='Заказы'))
    admin.add_view(PaymentView(Payment, db.session, name='Платежи'))


    admin.add_view(AnyPageView(name='Главная', endpoint='index'))


    with app.app_context():
        db.create_all()

    return app