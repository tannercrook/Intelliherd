# intelliherd/views/auth.py

from flask import current_app as app
from flask import Flask, Blueprint, render_template, flash, redirect, request, abort, url_for, session
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo, InputRequired
from sqlalchemy.orm import sessionmaker, scoped_session, query, session
import hashlib, uuid, secrets, string

from models.objects import SystemUser
from models.Connection import db_session

# set blueprint
public = Blueprint('public', __name__)

# This is the homepage for public users that will host the information and sign up features
@public.route('/')
def home():
    return render_template('public/index.html')




#  Form Classes 
# =================================================
class NewUserForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired(),EqualTo('password_confirm', message='Passwords must match')])
    password_confirm = PasswordField('Confirm Password', validators=[InputRequired()])


class ValidateForm(FlaskForm):
    code = StringField('Verification Code', validators=[InputRequired(), DataRequired()])

class OrgForm(FlaskForm):
    name = StringField('Organization Name', validators=[InputRequired(), DataRequired()])
