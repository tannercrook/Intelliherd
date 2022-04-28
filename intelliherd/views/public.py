# intelliherd/views/auth.py

from flask import current_app as app
from flask import Flask, Blueprint, render_template, flash, redirect, request, abort, url_for, session
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo, InputRequired
from sqlalchemy.orm import sessionmaker, scoped_session, query, session
from flask_mail import Mail, Message
import stripe
import hashlib, uuid, secrets, string

from models.objects import SystemUser, Subscription, OrgUser
from models.Connection import db_session

# set blueprint
public = Blueprint('public', __name__)

# This is the homepage for public users that will host the information and sign up features
@public.route('/')
def home():
    return render_template('public/index.html')


@public.route('/plans')
def plans():

    basicSubs = db_session.query(Subscription).filter(Subscription.training_included==0).filter(Subscription.price_monthly!='$0.00').order_by(Subscription.price_monthly.asc()).all()

    businessSubs = db_session.query(Subscription).filter(Subscription.name.like('Business%')).filter(Subscription.price_monthly!='$0.00').order_by(Subscription.price_monthly.asc()).all()

    enterpriseSubs = db_session.query(Subscription).filter(Subscription.name.like('Enterprise%')).filter(Subscription.price_monthly!='$0.00').order_by(Subscription.price_monthly.asc()).all()

    givingSubs = db_session.query(Subscription).filter(Subscription.price_monthly=='$0.00').all()

    return render_template('public/plans.html', basicSubs=basicSubs, businessSubs=businessSubs, enterpriseSubs=enterpriseSubs, givingSubs=givingSubs)





# Functions and routes to process new users and subscribers
# ======================================================================================================

# Step 1: Account
@public.route('/sign-up/<int:subscription_id>/account', methods=['GET','POST'])
def signUp(subscription_id):

    userForm = NewUserForm()
    if userForm.validate_on_submit():
        # Build the object
        user = SystemUser()
        user.email = userForm.email.data

        # Check to see if email already exists
        emailCount = db_session.query(SystemUser).filter(SystemUser.email==user.email).count()
        if emailCount > 0:
            flash('User with email already exists.', category='ERROR')
        else:
            user.first_name = userForm.first_name.data
            user.last_name = userForm.last_name.data
            user.salt = uuid.uuid4().hex
            user.password = hashlib.sha512(userForm.password.data.encode('utf-8')+user.salt.encode('utf-8')).hexdigest()

            alphabet = string.ascii_letters+string.digits
            user.maint_token = ''.join(secrets.choice(alphabet) for i in range(6))
            
            # Save the new record
            db_session.add(user)
            db_session.commit()

            mail = Mail(app)
            msg = Message('Intelliherd - Activate Account', sender='support@crooktec.com', recipients=[user.email])
            msg.body = 'Use the following code to activate your account: '+str(user.maint_token)
            mail.send(msg)

            return redirect(url_for('public.verifyNewAccount', subscription_id=subscription_id, user_id=user.user_id))

    return render_template('public/signup-account.html', userForm=userForm, subscription_id=subscription_id)


# Step 2: Verify Email
@public.route('/sign-up/<int:subscription_id>/account/<int:user_id>/verify', methods=['GET','POST'])
def verifyNewAccount(subscription_id, user_id):
    form = ValidateForm()

    if form.validate_on_submit():
        # get the code from the DB
        user = db_session.query(SystemUser).filter(SystemUser.user_id==user_id).one()
        # check to see that the combo of user_id and code match
        if user.maint_token == form.code.data:
            return redirect(url_for('public.createOrg', subscription_id=subscription_id, user_id=user_id))
        else:
            flash('Incorrect Verification Code. If problems persist, please contact support.', category='error')
            # TODO - Give option to have a new code sent


    return render_template('public/signup-verify.html', form=form)


# Step 3: Create Org
@public.route('/sign-up/<int:subscription_id>/account/<int:user_id>/create-org', methods=['GET','POST'])
def createOrg(subscription_id, user_id):
    orgForm = OrgForm()
    if orgForm.validate_on_submit():
        # Save the org
        org = Organization()
        org.name = orgForm.name.data 
        org.owner_id = user_id
        db_session.add(org)
        db_session.commit()

        # Save the org permissions
        role = Role()
        role.name = 'Organization Admin'
        role.organization_id = org.organization_id
        role.organization_mask = 777
        role.farm_mask = 777
        role.user_mask = 777
        role.animal_mask = 777
        db_session.add(role)
        db_session.commit()

        orgUser = OrgUser()
        orgUser.organization_id = org.organization_id
        orgUser.user_id = user_id
        orgUser.role_id = role.role_id
        db_session.add(orgUser)
        db_session.commit()


        return redirect(url_for('public.newAccountSuccess', subscription_id=subscription_id, user_id=user_id))

    return render_template('public/signup-org.html', form=orgForm)


@public.route('/sign-up/<int:subscription_id>/account/<int:user_id>/success', methods=['GET','POST'])
def newAccountSuccess(subscription_id, user_id):
    user = db_session.query(SystemUser).filter(SystemUser.user_id==user_id).one()
    return render_template('public/signup-success.html', user=user)

# ======================================================================================================






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
