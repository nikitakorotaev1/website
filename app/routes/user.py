from flask_login import login_user, logout_user
from wtforms.validators import email

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


@user_routes.route('/user/logout')
def logout():
    logout_user()
    return redirect(url_for('post.all'))