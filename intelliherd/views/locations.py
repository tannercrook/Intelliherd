
from flask import Flask, Blueprint, render_template, flash, redirect, request, abort, url_for, session
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, PasswordField
from wtforms.validators import DataRequired, Length, Email
from sqlalchemy.orm import sessionmaker, scoped_session, query
from flask_table import Table, Col

from models.objects import SystemUser, Organization, Role, Farm, FarmUser, Location
from models.Connection import db_session

# set blueprint
locations = Blueprint('locations', __name__, url_prefix='/locations')

@locations.route('/<int:farm_id>')
@login_required
def allLocations(farm_id):

    locations = db_session.query(Location).join(Organization).join(Farm).join(FarmUser).join(SystemUser, FarmUser.user_id==current_user.user_id).filter(Farm.farm_id==farm_id).all()

    # Get the farm
    farm = db_session.query(Farm).join(FarmUser).filter(Farm.farm_id==farm_id).one()

    # Build the table for locations
    table = LocationTable(locations)
    

    return render_template('locations/locations.html', current_user=current_user, orgLocations=locations, table=table, farm=farm)



class LocationTable(Table):
    classes = ['table','table-bordered']
    name = Col('Name')
    street_address = Col('Street Address')
    city = Col('City')
    state = Col('State')

