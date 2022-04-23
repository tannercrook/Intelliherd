

from flask import Flask, Blueprint, render_template, flash, redirect, request, abort, url_for, session, Response
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, PasswordField, TextAreaField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email
from sqlalchemy.orm import sessionmaker, scoped_session, query, session
from sqlalchemy.sql.functions import func
from flask_table import Table, Col, OptCol, LinkCol
import json

from models.objects import SystemUser, Organization, OrgUser, Farm, FarmUser, Animal, AnimalStatus, AnimalType, Vaccine, VaccineDose, Pen, PenMember, Relationship, RelationshipType
from models.Connection import db_session

# set blueprint
animals = Blueprint('animals', __name__)

# @animals.route('/')
# @login_required
# def allAnimals():

#     # Will return all animals that User has access to in a list
#     # TODO - Build list and template

#     return "Under Construction"





@animals.route('/farms/<int:farm_id>/animals/', methods=['GET','POST'])
@login_required
def animalsDashboard(farm_id):
    
    farm = db_session.query(Farm).join(FarmUser, FarmUser.farm_id==Farm.farm_id).filter(FarmUser.user_id==current_user.user_id).filter(Farm.farm_id==farm_id).one()
    
    # Get data for the widgets
    # TODO - Get data for the widgets on the dashboard
    animalCount = db_session.query(Animal).join(Farm).join(AnimalStatus).filter(Farm.farm_id == farm_id).filter(AnimalStatus.quota_apply==1).count()
    femaleCount = db_session.query(Animal).join(Farm).join(AnimalStatus).filter(Farm.farm_id == farm_id).filter(Animal.gender=='F').filter(AnimalStatus.quota_apply==1).count()
    maleCount = db_session.query(Animal).join(Farm).join(AnimalStatus).filter(Farm.farm_id == farm_id).filter(Animal.gender=='M').filter(AnimalStatus.quota_apply==1).count()
    # Counts for animal Status
    statusCounts = db_session.query(AnimalStatus.name, func.count(Animal.animal_status_id)).join(Animal).group_by(AnimalStatus.name).filter(AnimalStatus.active==1).all()
    statusLabels = []
    statusValues = []
    if len(statusCounts) > 0:
        for status in statusCounts:
            label = status[0]
            statusLabels.append(label)
            value = status[1]
            statusValues.append(value)



    return render_template('animals/animals-dashboard.html', current_user=current_user, farm=farm, animalCount = animalCount, femaleCount=femaleCount, maleCount=maleCount, statusLabels=statusLabels, statusValues=statusValues)



@animals.route('/farms/<int:farm_id>/animals/add-animal', methods=['GET','POST'])
@login_required
def addAnimal(farm_id):

    # Get the current farm (also checks permission)
    farm = db_session.query(Farm).join(FarmUser, FarmUser.farm_id==Farm.farm_id).filter(FarmUser.user_id==current_user.user_id).filter(Farm.farm_id==farm_id).one()
    
    # Set up the form for the new animal
    form = initializeAnimalForm()

    if form.is_submitted() and form.validate_on_submit():
        # handle the form data 

        # Create Animal Object
        animal = Animal()
        animal.farm_id = farm_id
        animal.animal_type_id = form.animal_type_id.data 
        animal.gender = form.gender.data 
        animal.birthdate = form.birthdate.data 
        animal.number = form.number.data 
        animal.name = form.name.data 
        animal.created_by = current_user.user_id
        animal.modified_by = current_user.user_id

        print(form.animal_type_id.data)
        print(form.gender.data)

        # Attempt to save the data to the DB
        db_session.add(animal)
        db_session.commit()
        
        flash("Saved Successfully")
        return redirect(url_for('animals.animalsDashboard', farm_id=farm_id))

        
        return "<h1>Under Construction</h1>"
    
    return render_template('animals/add-animal.html', current_user=current_user, farm=farm,form=form)


@animals.route('/farms/<int:farm_id>/animals/view', methods=['GET','POST'])
@login_required
def viewFarmAnimals(farm_id):
    # Get the current farm (also checks permission)
    farm = db_session.query(Farm).join(FarmUser, FarmUser.farm_id==Farm.farm_id).filter(FarmUser.user_id==current_user.user_id).filter(Farm.farm_id==farm_id).one()
    
    animals = db_session.query(Animal).join(Farm).filter(Farm.farm_id == farm_id).all()
    
    table = AnimalTable(animals)
    table.animal_type_id.choices = getAnimalTypes()

    return render_template('animals/farm-animals.html', current_user=current_user, farm=farm, table=table, animals=animals)

@animals.route('/farms/<int:farm_id>/animals/<int:animal_id>/view', methods=['GET','POST'])
@login_required
def viewAnimal(farm_id, animal_id):
    if hasAnimalRights(current_user.user_id, animal_id):
        form = initializeAnimalForm()
        animal = db_session.query(Animal).filter(Animal.animal_id==animal_id).one()
        farm = db_session.query(Farm).join(Animal).filter(Animal.animal_id==animal_id).one()
        user = db_session.query(SystemUser).filter(SystemUser.user_id==current_user.user_id).one()
        mother = db_session.query(Animal).join(Relationship, Relationship.parent_id==Animal.animal_id).join(RelationshipType).filter(RelationshipType.code=='MOTHER').filter(Relationship.animal_id==animal_id).first()
        father = db_session.query(Animal).join(Relationship, Relationship.parent_id==Animal.animal_id).join(RelationshipType).filter(RelationshipType.code=='FATHER').filter(Relationship.animal_id==animal_id).first()

        if form.validate_on_submit():
            animal.animal_type_id = form.animal_type_id.data 
            animal.number = form.number.data 
            animal.name = form.name.data 
            animal.gender = form.gender.data 
            animal.birthdate = form.birthdate.data 
            db_session.commit()
            flash('Animal Saved.', category='info')

        form.animal_type_id.data = animal.animal_type_id
        form.number.data = animal.number 
        form.name.data = animal.name
        form.gender.data = animal.gender
        form.birthdate.data = animal.birthdate

        return render_template('animals/view-animal.html', current_user=current_user, user=user, form=form, animal=animal, farm=farm, mother=mother, father=father)
    else: 
        flash("You don't have rights to this animal or it does not exist.", category='error')
        return redirect(url_for('animals.viewFarmAnimals', farm_id=farm_id))
    

@animals.route('/animals/<int:animal_id>/delete', methods=['GET','POST'])
@login_required
def deleteAnimal(animal_id):
    if hasAnimalRights(current_user.user_id, animal_id):
        animal = db_session.query(Animal).filter(Animal.animal_id==animal_id).one()
        farm = db_session.query(Farm).join(Animal).filter(Animal.animal_id==animal_id).one()
        db_session.delete(animal)
        db_session.commit()
        flash('Animal Deleted')
        return redirect(url_for('animals.viewFarmAnimals', farm_id = farm.farm_id))
    else: 
        return "You don't have rights to this animal or it does not exist."


# Vaccine Routes
# =============================================================================
@animals.route('/farms/<int:farm_id>/animals/<int:animal_id>/view/vaccines', methods=['GET','POST'])
def viewAnimalVaccines(farm_id, animal_id):
    if hasAnimalRights(current_user.user_id, animal_id):
        animal = db_session.query(Animal).filter(Animal.animal_id==animal_id).one()
        farm = db_session.query(Farm).join(Animal).filter(Animal.animal_id==animal_id).one()
        vaccineDoses = db_session.query(VaccineDose).join(Vaccine).join(Animal).filter(Animal.animal_id==animal_id).order_by(VaccineDose.date.desc()).all()
        table = VaccineDoseTable(vaccineDoses)
        table.vaccine_id.choices = getVaccines()
        table.recorded_by.choices = getUsers()
        return render_template('animals/animal-vaccines.html', current_user=current_user, farm=farm, animal=animal, table=table)
    else: 
        flash("You don't have rights to this animal or it does not exist.", category='error')
        return redirect(url_for('animals.viewFarmAnimals', farm_id=farm_id))

@animals.route('/farms/<int:farm_id>/animals/vaccine-wizard', methods=['GET','POST'])
@login_required
def vaccineWizard(farm_id):
    farm = db_session.query(Farm).join(FarmUser, FarmUser.farm_id==Farm.farm_id).filter(FarmUser.user_id==current_user.user_id).filter(Farm.farm_id==farm_id).one()

    # Get the Vaccines
    vaccines = []
    for r in db_session.query(Vaccine.vaccine_id, Vaccine.name).filter(Vaccine.active==1).all():
        vacDic = {'vaccine_id':r.vaccine_id, 'name':r.name}
        vaccines.append(vacDic)
    vaccinesJson = json.dumps(vaccines)

    # Get the Animals
    animalsDict = []
    for a in db_session.query(Animal.animal_id, Animal.number, Animal.name).join(AnimalStatus).filter(Animal.farm_id == farm_id).filter(AnimalStatus.quota_apply==1).all():
        animalDic = {'animal_id':a.animal_id,'number':a.number,'name':a.name}
        animalsDict.append(animalDic)
    animalsJson = json.dumps(animalsDict)

    return render_template('animals/vaccine-wizard.html', current_user=current_user, farm=farm, vaccines=vaccinesJson, animals=animalsJson)

@animals.route('/animals/vaccine-wizard/record/<int:animal_id>/<int:vaccine_id>', methods=['GET','POST'])
@login_required
def recordVaccineWizardDose(animal_id, vaccine_id):
    if hasAnimalRights(current_user.user_id, animal_id):
        vaccine = db_session.query(Vaccine).filter(Vaccine.vaccine_id==vaccine_id).one()
        animal = db_session.query(Animal).filter(Animal.animal_id==animal_id).one()
        try:
            dose = VaccineDose()
            dose.animal_id = animal_id
            dose.vaccine_id = vaccine_id
            dose.recorded_by = current_user.user_id
            db_session.add(dose)
            db_session.commit()
            return Response(json.dumps({'animal_number': animal.number,'animal_name':animal.name,'vaccine_name':vaccine.name,'status':'Recorded'}), status=201, mimetype="application/json")
        except:
            return Response(json.dumps({'Error': 'Internal Error'}), status=500, mimetype="application/json")
        return Response(json.dumps({'Error': 'Internal Error'}), status=500, mimetype="application/json")
    else:
        return Response(json.dumps({'Error': 'Internal Error'}), status=500, mimetype="application/json")


# Pen Routes
# ========================================================================================================
@animals.route('/farms/<int:farm_id>/animals/<int:animal_id>/view/pen-memberships', methods=['GET','POST'])
@login_required
def viewAnimalPenMemberships(farm_id, animal_id):
    if hasAnimalRights(current_user.user_id, animal_id):
        animal = db_session.query(Animal).filter(Animal.animal_id==animal_id).one()
        farm = db_session.query(Farm).join(Animal).filter(Animal.animal_id==animal_id).one()
    # Get the pen memberships
        penMemberships = db_session.query(PenMember).join(Animal, Animal.animal_id==PenMember.animal_id).join(Pen, PenMember.pen_id==Pen.pen_id).filter(Animal.animal_id==animal_id).order_by(PenMember.start_date, PenMember.end_date).all()
        table = PenMemberTable(penMemberships)
        table.pen_id.choices = getPenChoices(farm_id, excludeInactive=False)

        return render_template('animals/animal-penmemberships.html', current_user=current_user, farm=farm, animal=animal, table=table)
    else: 
        flash("You don't have rights to this animal or it does not exist.", category='error')
        return redirect(url_for('animals.viewFarmAnimals', farm_id=farm_id))




# Utility Functions
# ========================================================================================================
def initializeAnimalForm():
    # Initalizes the animal form with the select data
    form = AnimalForm()

    # Get animal_type choices
    animal_types = db_session.query(AnimalType.animal_type_id, AnimalType.name).all()
    form.animal_type_id.choices = animal_types

    return form





def getAnimalTypes():
    # Get animal_type choices
    animal_types = db_session.query(AnimalType.animal_type_id, AnimalType.name).all()

    return dict(animal_types)

def hasAnimalRights(user_id, animal_id):
    # Check to see if 
    animalCount = db_session.query(SystemUser).join(FarmUser, SystemUser.user_id==FarmUser.user_id).join(Animal, FarmUser.farm_id==Animal.farm_id).filter(SystemUser.user_id == user_id).filter(Animal.animal_id == animal_id).count()
    if animalCount >= 1:
        return True
    return False

def getVaccines():
    # Get vaccine choices
    vaccines = db_session.query(Vaccine.vaccine_id, Vaccine.name).all()
    return dict(vaccines)

def getUsers():
    # Get users
    users = db_session.query(SystemUser.user_id, SystemUser.first_name+' '+SystemUser.last_name).all()
    return dict(users)

def getPenChoices(farm_id, excludeInactive: bool):
    # Get pens for a farm
    if excludeInactive:
        pens = db_session.query(Pen.pen_id, Pen.name).join(Farm).filter(Farm.farm_id==farm_id).filter(Pen.active==1).all()
        return dict(pens)
    else:
        pens = db_session.query(Pen.pen_id, Pen.name).join(Farm).filter(Farm.farm_id==farm_id).all()
        return dict(pens)



# OBJECTS
# ========================================================================================================


# Class for adding new animals
class AnimalForm(FlaskForm):
    animal_type_id = SelectField('Animal Type:', coerce=int, validators=[DataRequired()])
    # TODO -  Implement breeds
    # breed_id = SelectField('Breed:')
    gender = SelectField('Gender:', choices=[('M','Male'),('F','Female')],validators=[DataRequired()])
    birthdate = DateField('Birthdate:')
    number = StringField('Number:', validators=[DataRequired()])
    name = StringField('Name:')
    # TODO -  Implement scanning data
    #scan_number = Column(Integer)






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


class VaccineDoseTable(Table):
    classes = ['table', 'table-bordered', 'table-striped', 'bg-white']
    table_id = 'vaccineDoseTable'
    no_items = 'Animal does not have any vaccine doses.'
    #view = LinkCol('View')
    vaccine_id = OptCol('Vaccine')
    date = Col('Date')
    recorded_by = OptCol('Recorder')
    recorded_date = Col('Recorded Date')
    

class PenMemberTable(Table):
    classes = ['table', 'table-bordered', 'table-striped', 'bg-white']
    table_id = 'penMemberTable'
    no_items = 'Animal does not have any current or historical Pen Memberships.'
    view = LinkCol('View', 'pens.editPenMembership', url_kwargs=dict(pen_id='pen_id', pen_member_id='pen_member_id'))
    pen_id = OptCol('Pen')
    start_date = Col('Start Date')
    end_date = Col('End Date')
