# coding: utf-8
import flask_login 
#from flask_jsontools import JsonSerializableBase
#from flask.ext.jsontools import JsonSerializableBase
from flask_login import UserMixin
from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String, Table, text, MetaData, Text, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import MONEY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import check_password_hash


import dateutil
import hashlib, uuid

Base = declarative_base()
metadata = Base.metadata


class Animal(Base):
    __tablename__ = 'animal'

    animal_id = Column(Integer, primary_key=True)
    farm_id = Column(ForeignKey('farm.farm_id'), nullable=False)
    animal_type_id = Column(ForeignKey('animal_type.animal_type_id'), nullable=False, server_default=text("1"))
    breed_id = Column(Integer)
    gender = Column(String(1), nullable=False, server_default=text("'F'::character varying"))
    birthdate = Column(Date)
    number = Column(String(60))
    name = Column(String(60))
    scan_number = Column(Integer)
    date_created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    created_by = Column(ForeignKey('system_user.user_id'), nullable=False, server_default=text("1"))
    date_modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified_by = Column(ForeignKey('system_user.user_id'), nullable=False, server_default=text("1"))
    animal_status_id = Column(ForeignKey('animal_status.animal_status_id'), nullable=False, server_default=text("1"))

    animal_status = relationship('AnimalStatus')
    animal_type = relationship('AnimalType')
    system_user = relationship('SystemUser', primaryjoin='Animal.created_by == SystemUser.user_id')
    farm = relationship('Farm')
    system_user1 = relationship('SystemUser', primaryjoin='Animal.modified_by == SystemUser.user_id')


class AnimalStatus(Base):
    __tablename__ = 'animal_status'

    animal_status_id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    active = Column(Integer, nullable=False, server_default=text("1"))
    quota_apply = Column(Integer, nullable=False, server_default=text("1"))
    code = Column(String(6), nullable=False)
    date_created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    created_by = Column(Integer, nullable=False, server_default=text("1"))
    date_modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified_by = Column(Integer, nullable=False, server_default=text("1"))


class AnimalType(Base):
    __tablename__ = 'animal_type'

    animal_type_id = Column(Integer, primary_key=True)
    name = Column(String(60), nullable=False)
    group_name = Column(String(60), nullable=False)
    active = Column(Integer, nullable=False, server_default=text("1"))


class Country(Base):
    __tablename__ = 'country'

    country_id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    abbreviation = Column(String(6))
    active = Column(Integer, nullable=False, server_default=text("1"))


class Farm(Base):
    __tablename__ = 'farm'

    farm_id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('system_user.user_id'), nullable=False)
    name = Column(String(60), nullable=False)
    location_id = Column(ForeignKey('location.location_id'), nullable=False)
    start_date = Column(Date, nullable=False, server_default=text("CURRENT_DATE"))
    end_date = Column(Date)
    date_created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    created_by = Column(ForeignKey('system_user.user_id'), nullable=False, server_default=text("1"))
    date_modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified_by = Column(ForeignKey('system_user.user_id'), nullable=False, server_default=text("1"))

    system_user = relationship('SystemUser', primaryjoin='Farm.created_by == SystemUser.user_id')
    location = relationship('Location')
    system_user1 = relationship('SystemUser', primaryjoin='Farm.modified_by == SystemUser.user_id')
    user = relationship('SystemUser', primaryjoin='Farm.user_id == SystemUser.user_id')


class Location(Base):
    __tablename__ = 'location'

    location_id = Column(Integer, primary_key=True)
    name = Column(String(60), nullable=False)
    street_address = Column(String(100), nullable=False)
    city = Column(String(60), nullable=False)
    state_id = Column(ForeignKey('state.state_id'), nullable=False)
    zip = Column(String(5), nullable=False)
    user_id = Column(ForeignKey('system_user.user_id'), nullable=False)

    state = relationship('State')
    user = relationship('SystemUser')


class Pen(Base):
    __tablename__ = 'pen'

    pen_id = Column(Integer, primary_key=True)
    farm_id = Column(ForeignKey('farm.farm_id', ondelete='CASCADE'), nullable=False)
    name = Column(String(60), nullable=False)
    location_id = Column(ForeignKey('location.location_id'))
    active = Column(Integer, nullable=False, server_default=text("1"))
    created_by = Column(ForeignKey('system_user.user_id'), nullable=False, server_default=text("1"))
    date_created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified_by = Column(ForeignKey('system_user.user_id'), nullable=False, server_default=text("1"))
    date_modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    max_occupancy = Column(Integer)

    system_user = relationship('SystemUser', primaryjoin='Pen.created_by == SystemUser.user_id')
    farm = relationship('Farm')
    location = relationship('Location')
    system_user1 = relationship('SystemUser', primaryjoin='Pen.modified_by == SystemUser.user_id')


class PenMember(Base):
    __tablename__ = 'pen_member'

    pen_member_id = Column(Integer, primary_key=True)
    pen_id = Column(ForeignKey('pen.pen_id', ondelete='CASCADE'), nullable=False)
    animal_id = Column(ForeignKey('animal.animal_id', ondelete='CASCADE'), nullable=False)
    start_date = Column(Date, nullable=False, server_default=text("CURRENT_DATE"))
    end_date = Column(Date)
    start_note = Column(Text)
    end_note = Column(Text)
    created_by = Column(ForeignKey('system_user.user_id'), nullable=False, server_default=text("1"))
    date_created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified_by = Column(ForeignKey('system_user.user_id'), nullable=False, server_default=text("1"))
    date_modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    animal = relationship('Animal')
    system_user = relationship('SystemUser', primaryjoin='PenMember.created_by == SystemUser.user_id')
    system_user1 = relationship('SystemUser', primaryjoin='PenMember.modified_by == SystemUser.user_id')
    pen = relationship('Pen')


class Relationship(Base):
    __tablename__ = 'relationship'

    relationship_id = Column(Integer, primary_key=True)
    animal_id = Column(ForeignKey('animal.animal_id', ondelete='CASCADE'), nullable=False)
    parent_id = Column(ForeignKey('animal.animal_id', ondelete='CASCADE'), nullable=False)
    relationship_type_id = Column(ForeignKey('relationship_type.relationship_type_id'), nullable=False)
    artificial = Column(Integer, nullable=False, server_default=text("0"))
    created_by = Column(ForeignKey('system_user.user_id'), nullable=False, server_default=text("1"))
    date_created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified_by = Column(ForeignKey('system_user.user_id'), nullable=False, server_default=text("1"))
    date_modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    animal = relationship('Animal', primaryjoin='Relationship.animal_id == Animal.animal_id')
    system_user = relationship('SystemUser', primaryjoin='Relationship.created_by == SystemUser.user_id')
    system_user1 = relationship('SystemUser', primaryjoin='Relationship.modified_by == SystemUser.user_id')
    parent = relationship('Animal', primaryjoin='Relationship.parent_id == Animal.animal_id')
    relationship_type = relationship('RelationshipType')


class RelationshipType(Base):
    __tablename__ = 'relationship_type'

    relationship_type_id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    code = Column(String(6), nullable=False)
    active = Column(Integer, nullable=False, server_default=text("1"))


class State(Base):
    __tablename__ = 'state'

    state_id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    abbreviation = Column(String(2), nullable=False)
    active = Column(Integer, nullable=False, server_default=text("1"))
    country_id = Column(ForeignKey('country.country_id'), nullable=False)

    country = relationship('Country')


class SystemUser(UserMixin, Base):
    __tablename__ = 'system_user'

    user_id = Column(Integer, primary_key=True)
    email = Column(String(60), nullable=False, unique=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    password = Column(String)
    salt = Column(String)
    date_created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    created_by = Column(ForeignKey('system_user.user_id'), nullable=False, server_default=text("1"))
    date_modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified_by = Column(ForeignKey('system_user.user_id'), nullable=False, server_default=text("1"))
    force_password_change = Column(Integer, nullable=False, server_default=text("0"))
    login_fail_count = Column(Integer, nullable=False, server_default=text("0"))
    admin = Column(Integer, nullable=False, server_default=text("0"))
    maint_token = Column(String)

    parent = relationship('SystemUser', remote_side=[user_id], primaryjoin='SystemUser.created_by == SystemUser.user_id')
    parent1 = relationship('SystemUser', remote_side=[user_id], primaryjoin='SystemUser.modified_by == SystemUser.user_id')
    
    # Custom class elements
    # ---------------------------------------------------
    # Flask-login Components

    @hybrid_property
    def id(self):
        return self.user_id

    def get_id(self):
        return self.user_id

    def passwordMatches(self, password):
        return check_password_hash(self.password, password)


    # AdminLTE Components
    @hybrid_property
    def full_name(self):
        return self.first_name+' '+self.last_name
    avatar = "#"
    @hybrid_property
    def created_at(self):
        return self.date_created


t_test = Table(
    'test', metadata,
    Column('testid', Integer),
    Column('name', String(30))
)


class TransactionLog(Base):
    __tablename__ = 'transaction_log'

    transaction_log_id = Column(Integer, primary_key=True)
    animal_id = Column(ForeignKey('animal.animal_id'), nullable=False)
    transaction_type_id = Column(ForeignKey('transaction_type.transaction_type_id'), nullable=False)
    title = Column(String(30), nullable=False)
    note = Column(Text)
    amount = Column(Numeric(12, 2), nullable=False, server_default=text("0.00"))
    created_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    created_by = Column(ForeignKey('system_user.user_id'), nullable=False)
    transaction_timestamp = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    animal = relationship('Animal')
    system_user = relationship('SystemUser')
    transaction_type = relationship('TransactionType')


class TransactionType(Base):
    __tablename__ = 'transaction_type'

    transaction_type_id = Column(Integer, primary_key=True)
    name = Column(String(60), nullable=False, unique=True)
    active = Column(Integer, server_default=text("1"))
    type = Column(String(30), nullable=False, server_default=text("'Expenditure'::character varying"))


class Vaccine(Base):
    __tablename__ = 'vaccine'

    vaccine_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    animal_type_id = Column(ForeignKey('animal_type.animal_type_id'), nullable=False)
    required = Column(Integer, nullable=False, server_default=text("0"))
    active = Column(Integer, nullable=False, server_default=text("1"))
    barcode = Column(String)
    created_by = Column(ForeignKey('system_user.user_id'), nullable=False, server_default=text("1"))
    date_created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified_by = Column(ForeignKey('system_user.user_id'), nullable=False, server_default=text("1"))
    date_modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    code = Column(String(6), nullable=False)

    animal_type = relationship('AnimalType')
    system_user = relationship('SystemUser', primaryjoin='Vaccine.created_by == SystemUser.user_id')
    system_user1 = relationship('SystemUser', primaryjoin='Vaccine.modified_by == SystemUser.user_id')


class VaccineDose(Base):
    __tablename__ = 'vaccine_dose'

    dose_id = Column(Integer, primary_key=True)
    animal_id = Column(ForeignKey('animal.animal_id', ondelete='CASCADE'), nullable=False)
    date = Column(Date, nullable=False, server_default=text("CURRENT_DATE"))
    recorded_by = Column(ForeignKey('system_user.user_id'), nullable=False)
    recorded_date = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    vaccine_id = Column(ForeignKey('vaccine.vaccine_id'), nullable=False)

    animal = relationship('Animal')
    system_user = relationship('SystemUser')
    vaccine = relationship('Vaccine')