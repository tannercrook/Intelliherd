from flask import Flask, Blueprint, render_template, flash, redirect, request, abort, url_for, session, Response
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, PasswordField, TextAreaField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, Optional
from sqlalchemy.orm import sessionmaker, scoped_session, query
from flask_table import Table, Col, OptCol, LinkCol

import datetime
import json

from models.objects import Farm, Animal, SystemUser, Pen, PenMember, AnimalType, AnimalStatus
from models.Connection import db_session

# set blueprint
pens = Blueprint('pens', __name__, url_prefix='/pens')

@pens.route('/<int:pen_id>', methods=['GET','POST'])
@login_required
def viewPen(pen_id):
    pen = db_session.query(Pen).filter(Pen.pen_id == pen_id).one()
    if(hasFarmRights(current_user.user_id, pen.farm_id)):
        # Get the farm
        farm = getFarm(pen_id)
        
        # Get the animals in the pen
        penAnimals = db_session.query(Animal).join(PenMember, Animal.animal_id==PenMember.animal_id).filter(PenMember.pen_id==pen_id).filter(PenMember.end_date==None).all()

        table = AnimalTable(penAnimals)
        table.animal_type_id.choices = getAnimalTypes()

        # Set up stats
        # TODO - Set up stats

        return render_template('pens/view-pen.html', current_user=current_user, farm=farm, pen=pen, table=table)


    else:
        return 'User does not have rights to this farm.'


@pens.route('/<int:pen_id>/wizard', methods=['GET','POST'])
@login_required
def penWizard(pen_id):
    pen = db_session.query(Pen).filter(Pen.pen_id == pen_id).one()
    if(hasFarmRights(current_user.user_id, pen.farm_id)):
        # Get the farm
        farm = getFarm(pen_id)

        animalsDict = []
        for a in db_session.query(Animal.animal_id, Animal.number, Animal.name).join(AnimalStatus).filter(Animal.farm_id == farm.farm_id).filter(AnimalStatus.quota_apply==1).all():
            animalDic = {'animal_id':a.animal_id,'number':a.number,'name':a.name}
            animalsDict.append(animalDic)
        animalsJson = json.dumps(animalsDict)

        return render_template('pens/pen-wizard.html', current_user=current_user, animals=animalsJson, pen=pen, farm=farm, pen_id=pen.pen_id)
    else:
        return 'User does not have rights to this farm.'

@pens.route('/<int:pen_id>/wizard/add/<int:animal_id>', methods=['GET','POST'])
@login_required 
def recordPenWizardAdd(pen_id, animal_id):
    if request.method == 'POST':
        pen = db_session.query(Pen).filter(Pen.pen_id == pen_id).one()
        if(hasFarmRights(current_user.user_id, pen.farm_id)):
            note = request.form['note']
            animal = db_session.query(Animal).join(Farm, Animal.farm_id == Farm.farm_id).filter(Animal.animal_id==animal_id).filter(Farm.farm_id==pen.farm_id).one()
            # Check if animal already has a Pen membership
            currentPenMemberID = getCurrentPenMembership(animal_id)
            if(currentPenMemberID != None):
                # End the previous
                currentPenMember = db_session.query(PenMember).filter(PenMember.pen_member_id==currentPenMemberID).one()
                currentPenMember.end_date = (datetime.date.today() - datetime.timedelta(days=1))
                currentPenMember.end_note = 'Moved via wizard.'
                currentPenMember.modified_by = current_user.user_id
                currentPenMember.date_modified = datetime.date.today()
                db_session.commit()
            try:
                penMember = PenMember()
                penMember.pen_id = pen.pen_id 
                penMember.animal_id = animal.animal_id
                penMember.start_date = datetime.date.today()
                penMember.start_note = note
                penMember.created_by = current_user.user_id
                penMember.modified_by = current_user.user_id
                db_session.add(penMember)
                db_session.commit()
                return Response(json.dumps({'animal_number': animal.number,'animal_name':animal.name,'pen_name':pen.name,'status':'Recorded'}), status=201, mimetype="application/json")
            except:
                return Response(json.dumps({'Error': 'Internal Error'}), status=500, mimetype="application/json")
        else:
            return Response(json.dumps({'Forbidden': 'No Access to Resource'}), status=403, mimetype="application/json")


@pens.route('/<int:pen_id>/wizard/record/<int:animal_id>', methods=['GET','POST'])
@login_required 
def recordPenWizardEnd(pen_id, animal_id):
    pen = db_session.query(Pen).filter(Pen.pen_id == pen_id).one()
    if(hasFarmRights(current_user.user_id, pen.farm_id)):
        note = request.args.get('note', default='', type=string)
        animal = db_session.query(Animal).join(Farm, Animal.farm_id == Farm.farm_id).filter(Farm.farm_id==pen.farm_id).one()
        try:
            penMember = PenMember()
            penMember.pen_id = pen.pen_id 
            penMember.animal_id = animal.animal_id
            penMember.end_date = date.today()
            penMember.end_note = note
            penMember.modified_by = current_user.user_id
            db_session.commit()
            return Response(json.dumps({'animal_number': animal.number,'animal_name':animal.name,'pen_name':pen.name,'status':'Recorded'}), status=201, mimetype="application/json")
        except:
            return Response(json.dumps({'Error': 'Internal Error'}), status=500, mimetype="application/json")
    else:
        return Response(json.dumps({'Forbidden': 'No Access to Resource'}), status=403, mimetype="application/json")



@pens.route('/<int:pen_id>/animals/<int:pen_member_id>', methods=['GET','POST'])
@login_required
def editPenMembership(pen_id, pen_member_id):
    pen = db_session.query(Pen).filter(Pen.pen_id == pen_id).one()
    farm = db_session.query(Farm).join(Pen).filter(Pen.pen_id==pen_id).one()
    if hasFarmRights(current_user.user_id, farm.farm_id):
        form = initializePenMemberForm(farm.farm_id)
        penMember = db_session.query(PenMember).filter(PenMember.pen_member_id==pen_member_id).one()
        if form.validate_on_submit():
            if form.end_date.data == None:
                # Check if animal already has a Pen membership
                animal = db_session.query(Animal).join(PenMember).filter(PenMember.pen_member_id==pen_member_id).one()
                currentPenMemberID = getCurrentPenMembership(animal.animal_id)
                if(currentPenMemberID != None):
                    flash('Not Saved: Conflicting active pen membership.', category='error')
                    penMember = db_session.query(PenMember).filter(PenMember.pen_member_id==pen_member_id).one()
                    form = fillPenMemberForm(farm.farm_id, form, penMember=penMember)
                    return redirect(url_for('pens.editPenMembership', pen_id=pen.pen_id, pen_member_id=penMember.pen_member_id))
            penMember.pen_id = form.pen_id.data
            penMember.start_date = form.start_date.data
            penMember.start_note = form.start_note.data 
            penMember.end_date = form.end_date.data
            penMember.end_note = form.end_note.data 
            db_session.commit()
            flash('Saved Successfully', category='info')

        penMember = db_session.query(PenMember).filter(PenMember.pen_member_id==pen_member_id).one()
        animal = db_session.query(Animal).join(PenMember).filter(PenMember.pen_member_id==pen_member_id).one()
        form = fillPenMemberForm(farm.farm_id, form, penMember=penMember)

        return render_template('animals/animal-edit-penmembership.html', current_user=current_user, farm=farm, animal=animal, penMember=penMember, form=form)
    else: 
        flash("You don't have rights to this animal or it does not exist.", category='error')
        return redirect(url_for('animals.viewFarmAnimals', farm_id=pen.farm_id))


@pens.route('/<int:pen_id>/animals/<int:pen_member_id>/delete', methods=['GET','POST'])
@login_required
def deletePenMember(pen_id, pen_member_id):
    pen = db_session.query(Pen).filter(Pen.pen_id == pen_id).one()
    if(hasFarmRights(current_user.user_id, pen.farm_id)):
        penMember = db_session.query(PenMember).filter(PenMember.pen_member_id==pen_member_id).one()
        db_session.delete(penMember)
        db_session.commit()
        flash('Pen Membership Deleted', category='info')
        return redirect(url_for('animals.viewAnimalPenMemberships', farm_id=pen.farm_id, animal_id=penMember.animal_id))
    else:
        flash('You do not have rights to this resource.', category='error')
        return redirect(url_for('animals.viewAnimalPenMemberships', farm_id=pen.farm_id, animal_id=penMember.animal_id))



def hasFarmRights(user_id, farm_id):
    # Check to see if 
    farmCount = db_session.query(SystemUser).join(Farm, SystemUser.user_id==Farm.user_id).filter(SystemUser.user_id == user_id).count()
    if farmCount >= 1:
        return True
    return False

def getAnimalTypes():
    # Get animal_type choices
    animal_types = db_session.query(AnimalType.animal_type_id, AnimalType.name).all()
    return dict(animal_types)

def getFarm(pen_id):
    # Get the farm for a pen
    farm = db_session.query(Farm).join(Pen, Farm.farm_id==Pen.farm_id).one()
    return farm

def getCurrentPenMembership(animal_id):
    penMembers = db_session.query(PenMember).filter(PenMember.animal_id==animal_id).filter(PenMember.end_date == None).all()
    if(len(penMembers) > 0):
        return penMembers[0].pen_member_id
    else:
        return None


def initializePenMemberForm(farm_id):
    form = PenMemberForm()
    form.pen_id.choices = getPenChoices(farm_id, excludeInactive=True)
    return form

def fillPenMemberForm(farm_id, form, penMember: PenMember):
    form.pen_id.choices = getPenChoices(farm_id, excludeInactive=True)
    form.pen_id.data = penMember.pen_id
    form.start_date.data = penMember.start_date
    form.start_note.data = penMember.start_note
    form.end_date.data = penMember.end_date
    form.end_note.data = penMember.end_note
    return form


def getPenChoices(farm_id, excludeInactive: bool):
    # Get pens for a farm
    if excludeInactive:
        pens = db_session.query(Pen.pen_id, Pen.name).join(Farm).filter(Farm.farm_id==farm_id).filter(Pen.active==1).all()
        return pens
    else:
        pens = db_session.query(Pen.pen_id, Pen.name).join(Farm).filter(Farm.farm_id==farm_id).all()
        return pens



# =======================================
# Classes 
# =======================================
# Animal Table Class
class AnimalTable(Table):
    classes = ['table','table-bordered','table-striped','bg-white']
    table_id = 'animalTable'
    no_items = 'Either the cows are out or they don\'t exist!'
    view = LinkCol('View', 'animals.viewAnimal', url_kwargs=dict(farm_id='farm_id', animal_id='animal_id'))
    number = Col('Number')
    name = Col('Name')
    gender = Col('Gender')
    birthdate = Col('Birthdate')
    animal_type_id = OptCol('Type')

class PenMemberForm(FlaskForm):
    pen_id = SelectField('Pen: ', coerce=int, validators=[DataRequired()])
    start_date = DateField('Start Date: ')
    start_note = TextAreaField('Start Note: ')
    end_date = DateField('End Date: ', validators=[Optional()] ,format='%Y-%m-%d')
    end_note = TextAreaField('End Note: ')

