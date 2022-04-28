# intelliherd/views/auth.py

from flask import Flask, Blueprint, render_template, flash, redirect, request, abort, url_for, session
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, PasswordField
from wtforms.validators import DataRequired, Length, Email
from sqlalchemy.orm import sessionmaker, scoped_session, query

from models.objects import SystemUser,
from models.Connection import db_session

# set blueprint
account = Blueprint('account', __name__, url_prefix='/account')

@account.route('/')
@login_required
def accountDashboard():


    return render_template('account/account-dashboard.html', current_user=current_user)