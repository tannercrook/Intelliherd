
import datetime
from flask import Flask, Blueprint, render_template, flash, redirect, request, abort, url_for, session
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, PasswordField
from wtforms.validators import DataRequired, Length, Email
from sqlalchemy.orm import sessionmaker, scoped_session, query

from models.objects import *
from models.Connection import db_session

# set blueprint
orgs = Blueprint('org', __name__, url_prefix='/org')


@orgs.route('/<int:org_id>', methods=['GET','POST'])
@login_required
def orgDashboard(org_id):
    
    # Get the users organization
    org = db_session.query(Organization).join(OrgUser).filter(Organization.organization_id==org_id).filter(OrgUser.user_id==current_user.user_id).one()


    # Check to see if the org has an active subscription
    subCount = db_session.query(OrgSubscription).join(Organization).filter(Organization.organization_id==org.organization_id).filter(OrgSubscription.end_date >= datetime.datetime.now()).count()

    if subCount == 0:
        # The org does not have a subscription. 
        return render_template('orgs/org-dashboard.html', current_user=current_user, org=org, orgSub=None, sub=None, farmCount=0, activeAnimals=0)
    else:
        orgSubscription = db_session.query(OrgSubscription).join(Organization).filter(Organization.organization_id==org.organization_id).filter(OrgSubscription.end_date >= datetime.datetime.now()).one()
        # Get the subscription
        subscription = db_session.query(Subscription).join(OrgSubscription).filter(Subscription.subscription_id==orgSubscription.subscription_id).one()

        # Get the count of farms
        farmCount = db_session.query(Farm).join(Organization).filter(Organization.organization_id==org.organization_id).count()

        # Get the count of animals and limit
        activeAnimals = db_session.query(Animal).join(Farm).join(Organization).join(AnimalStatus).filter(AnimalStatus.quota_apply==1).filter(Organization.organization_id==org_id).count()


    return render_template('orgs/org-dashboard.html', current_user=current_user, org=org, orgSub=orgSubscription, sub=subscription, farmCount=farmCount, activeAnimals=activeAnimals)