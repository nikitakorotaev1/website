from enum import unique

from ..extensions import db, login_manager
from datetime import datetime
from flask_login import UserMixin



class Role(db.Model):
    __tablename__ = 'role'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(250), nullable=False)


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone_number = db.Column(db.String(50), nullable=True, unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False, default=1)
    personnel_id = db.Column(db.Integer, db.ForeignKey('personnel.id'), nullable=True)

    personnel = db.relationship('Personnel', backref=db.backref('associated_user', uselist=False))
    role = db.relationship('Role', backref=db.backref('users', lazy=True))
    projects = db.relationship('Project', back_populates='client', lazy=True)
    client_orders = db.relationship('ClientOrder', backref='client', lazy=True)


class Personnel(db.Model):
    __tablename__ = 'personnel'


    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False, default=1)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=True)
    current_salary = db.Column(db.Numeric(10, 2), nullable=True)

    department = db.relationship('Department', backref=db.backref('employees', lazy=True), foreign_keys=[department_id])



class Department(db.Model):
    __tablename__ = 'department'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    department_name = db.Column(db.String(100), nullable=False)
    manager_id = db.Column(db.Integer, db.ForeignKey('personnel.id'), nullable=True)

    manager = db.relationship('Personnel', backref=db.backref('managed_department', uselist=False), foreign_keys=[manager_id])



class Project(db.Model):
    __tablename__ = 'project'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(250))
    description = db.Column(db.Text)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    client_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    manager_id = db.Column(db.Integer, db.ForeignKey('personnel.id'), nullable=True)

    department = db.relationship('Department', backref=db.backref('projects', lazy=True))
    client = db.relationship('User', back_populates='projects')
    manager = db.relationship('Personnel', backref=db.backref('managed_projects', lazy=True), foreign_keys=[manager_id])



class Finance(db.Model):
    __tablename__ = 'finance'

    finance_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=True)
    budget = db.Column(db.Numeric(15, 2), nullable=False)
    expenses = db.Column(db.Numeric(15, 2), nullable=False)
    income = db.Column(db.Numeric(15, 2), nullable=False, default=0)


class ClientOrder(db.Model):
    __tablename__ = 'client_order'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False, default=1)
    order_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(50), nullable=True)
    create_date = db.Column(db.DateTime, default=datetime.now, nullable=False)
    client_phone = db.Column(db.String(60), nullable=True)

    project = db.relationship('Project', backref='orders')



class Payment(db.Model):
    __tablename__ = 'payment'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('client_order.id'), nullable=False)
    payment_amount = db.Column(db.Numeric(15, 2), nullable=False)
    payment_date = db.Column(db.Date, nullable=False)
    payment_status = db.Column(db.String(50), nullable=True)




