# coding: utf-8
import flask_login 
from flask_jsontools import JsonSerializableBase
from flask_login import UserMixin
from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String, Table, text, MetaData, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import MONEY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property


import dateutil
import hashlib, uuid

Base = declarative_base(cls=(JsonSerializableBase))
metadata = Base.metadata


class Animal(Base):
    __tablename__ = 'animal'

    animal_id = Column(Integer, primary_key=True, server_default=text("nextval('animal_animal_id_seq'::regclass)"))
    farm_id = Column(ForeignKey(u'farm.farm_id'), nullable=False)
    animal_type_id = Column(ForeignKey(u'animal_type.animal_type_id'), nullable=False, server_default=text("1"))
    breed_id = Column(Integer)
    gender = Column(String(1), nullable=False, server_default=text("'F'::character varying"))
    birthdate = Column(Date)
    number = Column(String(60))
    name = Column(String(60))
    scan_number = Column(Integer)
    date_created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    created_by = Column(ForeignKey(u'system_user.user_id'), nullable=False, server_default=text("1"))
    date_modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified_by = Column(ForeignKey(u'system_user.user_id'), nullable=False, server_default=text("1"))
    animal_status_id = Column(ForeignKey(u'animal_status.animal_status_id'), nullable=False, server_default=text("1"))

    animal_status = relationship(u'AnimalStatus')
    animal_type = relationship(u'AnimalType')
    system_user = relationship(u'SystemUser', primaryjoin='Animal.created_by == SystemUser.user_id')
    farm = relationship(u'Farm')
    system_user1 = relationship(u'SystemUser', primaryjoin='Animal.modified_by == SystemUser.user_id')


class AnimalStatus(Base):
    __tablename__ = 'animal_status'

    animal_status_id = Column(Integer, primary_key=True, server_default=text("nextval('animal_status_animal_status_id_seq'::regclass)"))
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

    animal_type_id = Column(Integer, primary_key=True, server_default=text("nextval('animal_type_animal_type_id_seq'::regclass)"))
    name = Column(String(60), nullable=False)
    group_name = Column(String(60), nullable=False)
    active = Column(Integer, nullable=False, server_default=text("1"))


class SystemUser(UserMixin, Base):
    __tablename__ = 'system_user'

    user_id = Column(Integer, primary_key=True, server_default=text("nextval('user_user_id_seq'::regclass)"))
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
        hashedPassword = hashlib.sha512(str(password+self.salt).encode('utf-8')).hexdigest()
        if(hashedPassword == self.password):
            return True
        else:
            return False


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


class Organization(Base):
    __tablename__ = 'organization'

    organization_id = Column(Integer, primary_key=True, server_default=text("nextval('organization_organization_id_seq'::regclass)"))
    name = Column(String(60), nullable=False)
    date_created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    created_by = Column(ForeignKey('system_user.user_id'), nullable=False, server_default=text("1"))
    date_modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified_by = Column(ForeignKey('system_user.user_id'), nullable=False, server_default=text("1"))
    active = Column(Integer, nullable=False, server_default=text("1"))
    owner_id = Column(ForeignKey('system_user.user_id'), nullable=False, server_default=text("1"))

    system_user = relationship('SystemUser', primaryjoin='Organization.created_by == SystemUser.user_id')
    system_user1 = relationship('SystemUser', primaryjoin='Organization.modified_by == SystemUser.user_id')
    system_user2 = relationship('SystemUser', primaryjoin='Organization.owner_id == SystemUser.user_id')


class PaymentType(Base):
    __tablename__ = 'payment_type'

    payment_type_id = Column(Integer, primary_key=True, server_default=text("nextval('payment_type_payment_type_id_seq'::regclass)"))
    name = Column(String, nullable=False)
    code = Column(String(6), nullable=False)
    web_enabled = Column(Integer, nullable=False, server_default=text("0"))
    start_date = Column(Date, nullable=False, server_default=text("CURRENT_DATE"))
    end_date = Column(Date)
    date_created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    created_by = Column(ForeignKey('system_user.user_id'), nullable=False, server_default=text("1"))
    date_modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified_by = Column(ForeignKey('system_user.user_id'), nullable=False, server_default=text("1"))

    system_user = relationship('SystemUser', primaryjoin='PaymentType.created_by == SystemUser.user_id')
    system_user1 = relationship('SystemUser', primaryjoin='PaymentType.modified_by == SystemUser.user_id')


class Subscription(Base):
    __tablename__ = 'subscription'

    subscription_id = Column(Integer, primary_key=True, server_default=text("nextval('subscription_subscription_id_seq'::regclass)"))
    name = Column(String(60), nullable=False)
    max_farms = Column(Integer, nullable=False, server_default=text("1"))
    max_users = Column(Integer, nullable=False, server_default=text("1"))
    max_animals = Column(Integer, nullable=False, server_default=text("10"))
    start_date = Column(Date, nullable=False, server_default=text("CURRENT_DATE"))
    end_date = Column(Date)
    price_monthly = Column(MONEY, nullable=False, server_default=text("5.00"))
    price_annual = Column(MONEY, nullable=False, server_default=text("50.00"))
    training_included = Column(Integer, nullable=False, server_default=text("0"))
    support_included = Column(Integer, nullable=False, server_default=text("0"))
    date_created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    created_by = Column(ForeignKey('system_user.user_id'), nullable=False, server_default=text("1"))
    date_modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified_by = Column(ForeignKey('system_user.user_id'), nullable=False, server_default=text("1"))

    system_user = relationship('SystemUser', primaryjoin='Subscription.created_by == SystemUser.user_id')
    system_user1 = relationship('SystemUser', primaryjoin='Subscription.modified_by == SystemUser.user_id')


class Location(Base):
    __tablename__ = 'location'

    location_id = Column(Integer, primary_key=True, server_default=text("nextval('location_location_id_seq'::regclass)"))
    name = Column(String(60), nullable=False)
    street_address = Column(String(100), nullable=False)
    city = Column(String(60), nullable=False)
    state = Column(String(2), nullable=False)
    zip = Column(String(5), nullable=False)
    organization_id = Column(ForeignKey('organization.organization_id'), nullable=False)

    organization = relationship('Organization')


class PurchaseOrder(Base):
    __tablename__ = 'purchase_order'

    order_id = Column(Integer, primary_key=True, server_default=text("nextval('order_order_id_seq'::regclass)"))
    organization_id = Column(ForeignKey('organization.organization_id'), nullable=False)
    user_id = Column(ForeignKey('system_user.user_id'), nullable=False)
    processed_by = Column(ForeignKey('system_user.user_id'), nullable=False)
    payment_type_id = Column(Integer, nullable=False)
    date_placed = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    subscription_id = Column(ForeignKey('subscription.subscription_id'), nullable=False)
    total_amount = Column(MONEY)

    organization = relationship('Organization')
    system_user = relationship('SystemUser', primaryjoin='PurchaseOrder.processed_by == SystemUser.user_id')
    subscription = relationship('Subscription')
    user = relationship('SystemUser', primaryjoin='PurchaseOrder.user_id == SystemUser.user_id')


class Role(Base):
    __tablename__ = 'role'

    role_id = Column(Integer, primary_key=True, server_default=text("nextval('role_role_id_seq'::regclass)"))
    name = Column(String(60), nullable=False)
    organization_id = Column(ForeignKey('organization.organization_id'), nullable=False, server_default=text("nextval('role_organization_id_seq'::regclass)"))
    organization_mask = Column(Integer, nullable=False, server_default=text("0"))
    farm_mask = Column(Integer, nullable=False, server_default=text("0"))
    user_mask = Column(Integer, nullable=False, server_default=text("0"))
    animal_mask = Column(Integer, nullable=False, server_default=text("0"))
    active = Column(Integer, nullable=False, server_default=text("1"))
    date_created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    created_by = Column(ForeignKey('system_user.user_id'), nullable=False, server_default=text("1"))
    date_modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified_by = Column(ForeignKey('system_user.user_id'), nullable=False, server_default=text("1"))

    system_user = relationship('SystemUser', primaryjoin='Role.created_by == SystemUser.user_id')
    system_user1 = relationship('SystemUser', primaryjoin='Role.modified_by == SystemUser.user_id')
    organization = relationship('Organization')


class Farm(Base):
    __tablename__ = 'farm'

    farm_id = Column(Integer, primary_key=True, server_default=text("nextval('farm_farm_id_seq'::regclass)"))
    name = Column(String(60), nullable=False)
    organization_id = Column(ForeignKey('organization.organization_id'), nullable=False)
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
    organization = relationship('Organization')


class OrgSubscription(Base):
    __tablename__ = 'org_subscription'

    org_subscription_id = Column(Integer, primary_key=True, server_default=text("nextval('org_subscription_org_subscription_id_seq'::regclass)"))
    organization_id = Column(ForeignKey('organization.organization_id'), nullable=False)
    subscription_id = Column(ForeignKey('subscription.subscription_id'), nullable=False)
    start_date = Column(Date, nullable=False, server_default=text("CURRENT_DATE"))
    end_date = Column(Date, nullable=False)
    months_duration = Column(Integer, nullable=False, server_default=text("1"))
    order_id = Column(ForeignKey('purchase_order.order_id'), nullable=False)
    date_created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    created_by = Column(ForeignKey('system_user.user_id'), nullable=False, server_default=text("1"))
    date_modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified_by = Column(ForeignKey('system_user.user_id'), nullable=False, server_default=text("1"))
    auto_recurring = Column(Integer, nullable=False, server_default=text("0"))

    system_user = relationship('SystemUser', primaryjoin='OrgSubscription.created_by == SystemUser.user_id')
    system_user1 = relationship('SystemUser', primaryjoin='OrgSubscription.modified_by == SystemUser.user_id')
    order = relationship('PurchaseOrder')
    organization = relationship('Organization')
    subscription = relationship('Subscription')


class OrgUser(Base):
    __tablename__ = 'org_user'

    org_user_id = Column(Integer, primary_key=True, server_default=text("nextval('org_user_org_user_id_seq'::regclass)"))
    organization_id = Column(ForeignKey('organization.organization_id'), nullable=False)
    user_id = Column(ForeignKey('system_user.user_id'), nullable=False)
    role_id = Column(ForeignKey('role.role_id'), nullable=False)
    start_date = Column(Date, nullable=False, server_default=text("CURRENT_DATE"))
    end_date = Column(Date)
    date_created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    created_by = Column(ForeignKey('system_user.user_id'), nullable=False, server_default=text("1"))
    date_modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified_by = Column(ForeignKey('system_user.user_id'), nullable=False, server_default=text("1"))

    system_user = relationship('SystemUser', primaryjoin='OrgUser.created_by == SystemUser.user_id')
    system_user1 = relationship('SystemUser', primaryjoin='OrgUser.modified_by == SystemUser.user_id')
    organization = relationship('Organization')
    role = relationship('Role')
    user = relationship('SystemUser', primaryjoin='OrgUser.user_id == SystemUser.user_id')


class FarmUser(Base):
    __tablename__ = 'farm_user'

    farm_user_id = Column(Integer, primary_key=True)
    farm_id = Column(ForeignKey('farm.farm_id'), nullable=False)
    user_id = Column(ForeignKey('system_user.user_id'), nullable=False)
    role_id = Column(ForeignKey('role.role_id'), nullable=False)
    start_date = Column(Date, nullable=False, server_default=text("CURRENT_DATE"))
    end_date = Column(Date)
    date_created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    created_by = Column(ForeignKey('system_user.user_id'), nullable=False, server_default=text("1"))
    date_modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified_by = Column(ForeignKey('system_user.user_id'), nullable=False, server_default=text("1"))

    system_user = relationship('SystemUser', primaryjoin='FarmUser.created_by == SystemUser.user_id')
    farm = relationship('Farm')
    system_user1 = relationship('SystemUser', primaryjoin='FarmUser.modified_by == SystemUser.user_id')
    role = relationship('Role')
    user = relationship('SystemUser', primaryjoin='FarmUser.user_id == SystemUser.user_id')



class Vaccine(Base):
    __tablename__ = 'vaccine'

    vaccine_id = Column(Integer, primary_key=True, server_default=text("nextval('newtable_vaccine_id_seq'::regclass)"))
    name = Column(String(100), nullable=False)
    animal_type_id = Column(ForeignKey(u'animal_type.animal_type_id'), nullable=False)
    required = Column(Integer, nullable=False, server_default=text("0"))
    active = Column(Integer, nullable=False, server_default=text("1"))
    barcode = Column(String)
    created_by = Column(ForeignKey(u'system_user.user_id'), nullable=False, server_default=text("1"))
    date_created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified_by = Column(ForeignKey(u'system_user.user_id'), nullable=False, server_default=text("1"))
    date_modified = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    code = Column(String(6), nullable=False)

    animal_type = relationship(u'AnimalType')
    system_user = relationship(u'SystemUser', primaryjoin='Vaccine.created_by == SystemUser.user_id')
    system_user1 = relationship(u'SystemUser', primaryjoin='Vaccine.modified_by == SystemUser.user_id')



class VaccineDose(Base):
    __tablename__ = 'vaccine_dose'

    dose_id = Column(Integer, primary_key=True, server_default=text("nextval('vaccine_dose_dose_id_seq'::regclass)"))
    animal_id = Column(ForeignKey(u'animal.animal_id', ondelete=u'CASCADE'), nullable=False)
    date = Column(Date, nullable=False, server_default=text("CURRENT_DATE"))
    recorded_by = Column(ForeignKey(u'system_user.user_id'), nullable=False)
    recorded_date = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    vaccine_id = Column(ForeignKey(u'vaccine.vaccine_id'), nullable=False)

    animal = relationship(u'Animal')
    system_user = relationship(u'SystemUser')
    vaccine = relationship(u'Vaccine')

class Pen(Base):
    __tablename__ = 'pen'

    pen_id = Column(Integer, primary_key=True, server_default=text("nextval('pen_pen_id_seq'::regclass)"))
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

    pen_member_id = Column(Integer, primary_key=True, server_default=text("nextval('pen_member_pen_member_id_seq'::regclass)"))
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

    relationship_id = Column(Integer, primary_key=True, server_default=text("nextval('relationship_relationship_id_seq'::regclass)"))
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

    relationship_type_id = Column(Integer, primary_key=True, server_default=text("nextval('relationship_type_relationship_type_id_seq'::regclass)"))
    name = Column(String(20), nullable=False)
    code = Column(String(6), nullable=False)
    active = Column(Integer, nullable=False, server_default=text("1"))