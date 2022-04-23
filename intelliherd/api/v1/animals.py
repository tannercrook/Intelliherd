# api/animals.py

from flask import Flask, request, Blueprint, jsonify
from sqlalchemy.orm import sessionmaker, scoped_session, query
from models.objects import SystemUser, Organization, Role, Farm, Animal
from models.Connection import db_session
import json

# set blueprint
apiAnimals = Blueprint('apiAnimals', __name__, url_prefix='/api/v1/animals')

@apiAnimals.route('/<int:farm_id>', methods=['GET'])
def get(farm_id):
    # TODO-Authenticate the token
    token = request.args.get('token')
    print(token)

    if (request.args.get('animal_id') != None):
        animals = db_session.query(Animal).filter(Animal.farm_id==farm_id).filter(Animal.animal_id==request.args.get('animal_id'))
    elif (request.args.get('gender') != None):
        animals = db_session.query(Animal).filter(Animal.farm_id==farm_id).filter(Animal.gender==request.args.get('gender'))
    elif (request.args.get('number') != None):
        animals = db_session.query(Animal).filter(Animal.farm_id==farm_id).filter(Animal.number==request.args.get('number'))
    elif (request.args.get('name') != None):
        animals = db_session.query(Animal).filter(Animal.farm_id==farm_id).filter(Animal.name==request.args.get('name'))
    else:
        animals = db_session.query(Animal).filter(Animal.farm_id==farm_id).all()

    animalsJson = []

    for animal in animals:
        animalsJson.append(animal.__json__())

    return json.dumps(animalsJson, indent=4, sort_keys=True, default=str), 200, {'content-type': 'application/json'}


