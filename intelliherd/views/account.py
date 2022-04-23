# intelliherd/views/auth.py

from flask import Flask, Blueprint, render_template, flash, redirect, request, abort, url_for, session
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, PasswordField
from wtforms.validators import DataRequired, Length, Email
from sqlalchemy.orm import sessionmaker, scoped_session, query

from models.objects import SystemUser, Organization, Role 
from models.Connection import db_session

# set blueprint
account = Blueprint('account', __name__, url_prefix='/account')

@account.route('/')
@login_required
def accountDashboard():

    # See if the user is owner of an Org
    orgCount = db_session.query(SystemUser).join(Organization, Organization.owner_id==SystemUser.user_id).filter(SystemUser.user_id == current_user.user_id).count()
    org = None
    if orgCount > 0:
        org = db_session.query(Organization).join(SystemUser, Organization.owner_id==SystemUser.user_id).filter(SystemUser.user_id == current_user.user_id).filter(Organization.active == 1).one()
        print(org)
    data = {
        "orgCount":orgCount,
        "org":org
    }


    return render_template('account/account-dashboard.html', current_user=current_user, org=org, data=data)