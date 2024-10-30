from xml.dom import ValidationErr

from flask_wtf import FlaskForm
from sqlalchemy import Boolean
from wtforms.fields.simple import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError

from .models.data import User


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    name = StringField('Логин', validators=[DataRequired(), Length(min=8, max=20)])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=8, max=20)])
    confirm_password = PasswordField('Подтвердите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')


    def validate_name(self, name):
        user = User.query.filter_by(name=name.data).first()
        if user:
            raise ValidationError("Имя пользователя занято")

class LoginForm(FlaskForm):
    name = StringField('Логин', validators=[DataRequired(), Length(min=8, max=20)])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=8, max=20)])
    remember = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')



