

from flask import Flask, Blueprint, render_template, flash, redirect, request, abort, url_for, session
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email
from sqlalchemy.orm import sessionmaker, scoped_session, query
from flask_table2 import Table, Col, OptCol, LinkCol
from models.objects import SystemUser, Farm, Pen, PenMember
from models.Connection import db_session

# set blueprint
farms = Blueprint('farms', __name__, url_prefix='/farms')

@farms.route('/')
@login_required
def allFarms():

    # See if the user has any farms available. If not, forward to the get subscription page
    farmCount = db_session.query(SystemUser).join(Farm, SystemUser.user_id == Farm.user_id).filter(SystemUser.user_id==current_user.user_id).count()

    if farmCount == 0:
        # TODO - User does not have any farms, let them know and offer subscription
        print("No farms for"+str(current_user.user_id))
    else:
        # User has one or more rights to a farm.
        # Get the farms
        userFarms = []
        userFarms = db_session.query(Farm).filter(Farm.user_id==current_user.user_id).all()

        return render_template('farms/farms.html', current_user=current_user, userFarms=userFarms)





@farms.route('/<int:farm_id>', methods=['GET','POST'])
@login_required
def farmDashboard(farm_id):
    
    farm = db_session.query(Farm).filter(Farm.user_id==current_user.user_id).filter(Farm.farm_id==farm_id).one()
    
    # Get data for the widgets
    # TODO - Get data for the widgets on the dashboard


    return render_template('farms/farm-dashboard.html', current_user=current_user, farm=farm)


@farms.route('/<int:farm_id>/pens', methods=['GET','POST'])
@login_required
def pensDashboard(farm_id):
    farm = db_session.query(Farm).filter(Farm.user_id==current_user.user_id).filter(Farm.farm_id==farm_id).one()

    # Get the pens
    pens = db_session.query(Pen).join(Farm).filter(Farm.farm_id == farm.farm_id).order_by(Pen.name.asc())

    # Set up the table
    table = PenTable(pens)


    return render_template('pens/pen-dashboard.html', current_user=current_user, farm=farm, pens=pens, table=table)


@farms.route('/<int:farm_id>/pens/create', methods=['GET','POST'])
@login_required 
def createPen(farm_id):
    farm = db_session.query(Farm).filter(Farm.user_id==current_user.user_id).filter(Farm.farm_id==farm_id).one()

    form = PenForm()
    form.active.data = 1

    if form.validate_on_submit():
        pen = Pen()
        pen.farm_id = farm_id
        pen.name = form.name.data 
        pen.active = form.active.data 
        pen.max_occupancy = form.max_occupancy.data
        pen.created_by = current_user.user_id
        pen.modified_by = current_user.user_id

        # Save to database
        db_session.add(pen)
        db_session.commit()
        flash("Successfully added pen.")
        return redirect(url_for('farms.pensDashboard', farm_id=farm_id))

    return render_template('pens/create-pen.html', current_user=current_user, farm=farm, form=form)




# Classes
# =====================================================================


# New pen form
class PenForm(FlaskForm):
    name = StringField('Name: ', validators=[DataRequired()])
    max_occupancy = IntegerField('Max Occupancy: ')
    active = BooleanField('Active: ')
    # TODO - Add location feature 
    submit = SubmitField('Save: ')



# Animal Table Class
class PenTable(Table):
    classes = ['table','table-bordered','table-striped','bg-white']
    table_id = 'penTable'
    no_items = 'You do not have any pens yet!'
    view = LinkCol('View', 'pens.viewPen', url_kwargs=dict(pen_id='pen_id'))
    name = Col('Name')
    active = Col('Active')
    max_occupancy = Col('Max Occupancy')
