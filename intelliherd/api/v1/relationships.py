# api/animals.py

from flask import Flask, request, Blueprint, jsonify, Response
from sqlalchemy.orm import sessionmaker, scoped_session, query
from models.objects import SystemUser, Organization, Role, Farm, Animal, RelationshipType, Relationship
from models.Connection import db_session
import json

# set blueprint
apiRelationships = Blueprint('apiRelationships', __name__, url_prefix='/api/v1/relationships')

@apiRelationships.route('/', methods=['GET'])
def get():
    # TODO-Authenticate the token
    token = request.args.get('token')
    print(token)

    if (request.args.get('animal_id') != None):
        result = db_session.query(Relationship).filter(Relationship.animal_id==request.args.get('animal_id')).all()
    elif (request.args.get('parent_id') != None):
        result = db_session.query(Relationship).filter(Relationship.parent_id==request.args.get('parent_id')).all()
    else:
        result = db_session.query(Relationship).all()

    jsonList = []

    for r in result:
        jsonList.append(r.__json__())

    return json.dumps(jsonList, indent=4, sort_keys=True, default=str), 200, {'content-type': 'application/json'}

@apiRelationships.route('/', methods=['PUT'])
def put():
    # TODO-Check that user is owner of animal
    new = Relationship()
    new.animal_id = request.args.get('animal_id')
    new.parent_id = request.args.get('parent_id')
    new.relationship_type_id = request.args.get('relationship_type_id')
    user = db_session.query(SystemUser).filter(SystemUser.password==request.args.get('token')).one()
    new.created_by = user.user_id
    new.modified_by = user.user_id
    db_session.add(new)
    db_session.commit()
    return Response(status=201, mimetype="application/json")

@apiRelationships.route('/<int:relationship_id>', methods=['DELETE'])
def delete(relationship_id):
    # TODO-Check that user is owner of animal
    result = db_session.query(Relationship).filter(Relationship.relationship_id==relationship_id).one()

    if (result != None):
        db_session.delete(result)
        db_session.commit()
        return Response(status=200, mimetype="application/json")

    return Response(status=204, mimetype="application/json")


@apiRelationships.route('/unlink', methods=['DELETE'])
def deletePair():
    # Will delete a relationship when the animal_id and parent_id are given

    # TODO-Check that user is owner of animal
    animal_id = request.args.get('animal_id')
    parent_id = request.args.get('parent_id')
    result = db_session.query(Relationship).filter(Relationship.animal_id==animal_id).filter(Relationship.parent_id==parent_id).first()

    if (result != None):
        db_session.delete(result)
        db_session.commit()
        return Response(status=200, mimetype="application/json")

    return Response(status=204, mimetype="application/json")


# Relationship Types
@apiRelationships.route('/types/', methods=['GET'])
def getTypes():
    result = db_session.query(RelationshipType)
    jsonList = []

    for r in result:
        jsonList.append(r.__json__())

    return json.dumps(jsonList, indent=4, sort_keys=True, default=str), 200, {'content-type': 'application/json'}
