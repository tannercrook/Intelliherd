# api/farm.py

from flask import Flask, request, Blueprint, jsonify
from sqlalchemy.orm import sessionmaker, scoped_session, query
from models.objects import SystemUser, Farm,  Pen, PenMember
from models.Connection import db_session
import json

# set blueprint
apiFarm = Blueprint('apiFarm', __name__, url_prefix='/api/v1/farm')

@apiFarm.route('/<int:farm_id>', methods=['GET'])
def get(farm_id):
    # TODO-Authenticate the token
    token = request.args.get('token')
    print(token)

    # TODO-Get farm data
    farm = db_session.query(Farm).filter(Farm.farm_id==farm_id).one()

    return farm.__json__()

