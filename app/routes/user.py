from flask_login import login_user, logout_user, login_required, current_user
from wtforms.validators import email

from ..models.data import ClientOrder, Project, Finance
from ..models.post import Post
from ..forms import RegistrationForm, LoginForm
from ..extensions import db, bcrypt, login_manager
from flask import Blueprint, render_template, redirect, flash, url_for, request
from ..models.data import User

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/user/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data ,name=form.name.data, password=hashed_password)

        try:
            db.session.add(user)
            db.session.commit()
            flash(f"Поздравляем, {form.name.data}, вы зарегистрированы!", "success")
            return redirect(url_for('user_routes.login'))
        except Exception as e:
            print(str(e))
            flash(f"При регистрации произошла ошибка", "danger")
    return render_template('login/register.html', form=form)


@user_routes.route('/user/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.name.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('post.all'))
        else:
            flash(f"Ошибка входа. Неверное имя пользователя или пароль")

    return render_template('login/login.html', form=form)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Выход из аккаунта
@user_routes.route('/user/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('post.all'))


# Профиль пользователя
@user_routes.route('/user/profile', methods=['GET', 'POST'])
@login_required
def profile():
    profile = User.query.filter_by(name=current_user.name).first()
    current_user.name = profile.name
    db.session.commit()
    return render_template('account/profile.html', user=current_user)

@user_routes.route('/user/updatephone', methods=['POST'])
@login_required
def update_phone():
    phone_number = request.form.get('phone_number')
    if not phone_number:
        flash('Введите номер телефона', 'danger')
    elif not phone_number.startswith('+'):
        flash('Номер телефона должен начинаться с "+"', 'danger')
    else:
        current_user.phone_number = phone_number
        try:
            db.session.commit()
            flash('Номер телефона успешно обновлен!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка: {e}', 'danger')
    return redirect(url_for('post.all'))



# Заказы пользователя
@user_routes.route('/user/orders', methods=['GET', 'POST'])
@login_required
def user_orders():
    user_orders = ClientOrder.query.filter_by(client_id=current_user.id).all()
    return render_template('account/orders.html', user=current_user, orders=user_orders)


@user_routes.route('/user/projects', methods=['GET', 'POST'])
@login_required
def user_projects():

    if not current_user.is_authenticated or current_user.role.id != 3:
        return redirect(url_for('post.all'))

    if not current_user.personnel:
        return redirect(url_for('post.all'))

    user_projects = Project.query.filter_by(manager_id=current_user.personnel.id).all()
    return render_template('account/projects.html', projects=user_projects, user=current_user)

@user_routes.route('/user/finances', methods=['GET', 'POST'])
@login_required
def user_finances():

    if not current_user.is_authenticated or current_user.role.id != 3:
        return redirect(url_for('post.all'))

    user_projects = Project.query.filter_by(manager_id=current_user.id).all()

    project_finances = {
        project: Finance.query.filter_by(project_id=project.id).all()
        for project in user_projects
    }


    return render_template('account/finances.html', project_finances=project_finances, user=current_user)

