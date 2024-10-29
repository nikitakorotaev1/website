from flask import Flask

from .extensions import db, migrate
from .config import Config

# from .routes.user import user
from .routes.post import post
from .models.data import *
from .models.admin import AnyPageView, DashboardView
from .models.post import Post

from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # app.register_blueprint(user)
    app.register_blueprint(post)


    db.init_app(app)
    migrate.init_app(app, db)

   # Создание панели управления через flask-admin

    admin = Admin(app, name='Панель Управления', template_mode='bootstrap3', index_view=DashboardView(), endpoint='admin')
    admin.add_view(ModelView(Role, db.session, name='Роль'))
    admin.add_view(ModelView(User, db.session, name='Пользователи'))
    admin.add_view(ModelView(Personnel, db.session, name='Персонал'))
    admin.add_view(ModelView(Department, db.session, name='Отделы'))
    admin.add_view(ModelView(Project, db.session, name='Проекты'))
    admin.add_view(ModelView(Finance, db.session, name='Финансы'))
    admin.add_view(ModelView(ClientOrder, db.session, name='Заказы'))
    admin.add_view(ModelView(Payment, db.session, name='Платежи'))

    admin.add_view(AnyPageView(name='Главная', endpoint='index'))

    with app.app_context():
        db.create_all()

    return app