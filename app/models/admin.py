from flask import flash, redirect, url_for
from flask_login import login_required, current_user
from flask_admin.contrib.sqla import ModelView

from ..extensions import db
from flask_admin import BaseView, expose, AdminIndexView
from .data import *

class AnyPageView(BaseView):
    @expose('/')
    @login_required
    def any_page(self):
        return self.render('admin/anypage/index.html')


class DashboardView(AdminIndexView):
    @expose('/')
    @login_required
    def index(self):
        # Проверка, что пользователь имеет административные права
        if not current_user.is_authenticated or current_user.role.id != 2:
            return redirect(url_for('post.all'))  # Перенаправление на главную страницу

        all_users = User.query.all()
        return self.render('admin/dashboard.html', all_users=all_users)


class AdminModelView(ModelView):
    # Проверка роли
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role.title == 'Админ'

    def inaccessible_callback(self, name, **kwargs):
        flash("У вас нет прав для доступа в панель администратора", "error")
        return redirect(url_for('post.all'))



class PersonnelView(AdminModelView):
    # Настройка отображаемых колонок
    column_list = ('id', 'first_name', 'last_name', 'birthdate', 'role_id', 'department_id', 'current_salary', 'associated_user')

    # Настройка колонок, доступных для редактирования в форме
    form_columns = ('first_name', 'last_name', 'birthdate', 'role_id', 'department_id', 'current_salary', )

    # Дополнительно, можно добавить фильтры
    column_filters = ('first_name', 'last_name', 'birthdate', 'role_id', 'department_id', 'current_salary', 'associated_user')

    # Настройка сортировки
    column_sortable_list = ('id', 'first_name', 'last_name', 'birthdate', 'current_salary')

    column_formatters = {
        'associated_user': lambda v, c, m, p: m.associated_user.name if m.associated_user else 'Нет пользователя'
    }

    column_labels = {
        'id': 'ID',
        'first_name': 'Имя',
        'last_name': 'Фамилия',
        'birthdate': 'Дата рождения',
        'role_id': 'Роль',
        'department_id': 'Отдел',
        'current_salary': 'Текущая зарплата',
        'associated_user': 'Пользователь'
    }


class RoleView(AdminModelView):
    edit_template = 'admin/model/custom_edit.html'
    list_template = 'admin/model/custom_list.html'
    column_list = ('id', 'title')
    form_columns = ('title',)

    column_labels = {
        'id': 'ID',
        'title': 'Название'
    }

class UserView(AdminModelView):
    column_list = ('id', 'name', 'email', 'phone_number', 'role_id', 'personnel_id')
    form_columns = ('name', 'password', 'email', 'phone_number', 'role_id', 'personnel_id')
    column_filters = ('name', 'email', 'personnel_id')
    column_searchable_list = ('name', 'email')

    column_labels = {
        'id': 'ID',
        'name': 'Имя пользователя',
        'phone_number': 'Номер телефона',
        'role_id': 'Роль',
        'personnel_id': 'ID Сотрудника'
    }


class DepartmentView(AdminModelView):
    column_list = ('id', 'department_name', 'manager_id')
    form_columns = ('department_name', 'manager_id')

    column_labels = {
        'id': 'ID',
        'department_name': 'Отдел',
        'manager_id': 'ID Руководителя'
    }


class ProjectView(AdminModelView):
    column_list = ('id', 'title', 'description', 'start_date', 'end_date', 'department_id', 'client_id')
    form_columns = ('title', 'description', 'start_date', 'end_date', 'department_id', 'client_id')

    column_labels = {
        'id': 'ID',
        'title': 'Название',
        'description': 'Описание',
        'start_date': 'Дата начала',
        'end_date': 'Дата окончания',
        'department_id': 'ID Отдела',
        'client_id': 'ID Заказчика'
    }

class FinanceView(AdminModelView):
    column_list = ('finance_id', 'project_id', 'budget', 'expenses', 'income')
    form_columns = ('project_id', 'budget', 'expenses', 'income')
    column_filters = ('budget', 'expenses', 'income')

    column_labels = {
        'id': 'ID',
        'project_id': 'ID Проекта',
        'budget': 'Бюджет',
        'expenses': 'Расходы',
        'income': 'Прибыль'
    }

class ClientOrderView(AdminModelView):
    column_list = ('id', 'client_id', 'project_id', 'order_date', 'status', 'create_date', 'client_phone')
    form_columns = ('client_id', 'project_id', 'order_date', 'status', 'client_phone')
    column_filters = ('status', 'client_id', 'order_date')
    column_searchable_list = ('status', 'client_phone')

    column_labels = {
        'id': 'ID',
        'client_id': 'ID Заказчика',
        'project_id': 'ID Проекта',
        'order_date': 'Дата заказа',
        'status': 'Статус',
        'create_date': 'Время создания',
        'client_phone': 'Телефон заказчика',
    }

class PaymentView(AdminModelView):
    column_list = ('id', 'order_id', 'payment_amount', 'payment_date', 'payment_status')
    form_columns = ('order_id', 'payment_amount', 'payment_date', 'payment_status')
    column_filters = ('payment_status', 'payment_date')

    column_labels = {
        'id': 'ID',
        'order_id': 'ID заказаx',
        'payment_amount': 'Сумма платежа',
        'payment_date': 'Дата платежа',
        'payment_status': 'Статус платежа'
    }



