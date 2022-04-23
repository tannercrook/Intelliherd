# intelliherd/views/auth.py

from flask import Flask, Blueprint, render_template, flash, redirect, request, abort, url_for, session
from flask_login import LoginManager, login_required, login_user, logout_user 
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, PasswordField
from wtforms.validators import DataRequired, Length, Email
from sqlalchemy.orm import sessionmaker, scoped_session, query

from models.objects import SystemUser, Base, UserMixin 
from models.Connection import db_session

# set blueprint
auth = Blueprint('auth', __name__)

@auth.route('/auth/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print("here")
        user = db_session.query(SystemUser).filter(SystemUser.email == form.email.data).one()
        if (user != None):
            if user.passwordMatches(form.password.data):
                session['user_id'] = user.user_id
                login_user(user)
                next = request.args.get('next')
                if next is None or not next.startswith('/'):
                    next = url_for('account.accountDashboard')
                return redirect(next)
        flash('Invalid username or password.')
    

    return render_template('account/login.html', form=form)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


class LoginForm(FlaskForm):
    email = StringField('Email:', validators=[DataRequired(), Length(1,64),Email()])
    password = PasswordField('Password:', validators=[DataRequired()])
    submit = SubmitField('Login')
