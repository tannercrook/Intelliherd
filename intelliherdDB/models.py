# coding: utf-8
from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String, Table, text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import MONEY
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class AnimalType(Base):
    __tablename__ = 'animal_type'

    animal_type_id = Column(Integer, primary_key=True, server_default=text("nextval('animal_type_animal_type_id_seq'::regclass)"))
    name = Column(String(60), nullable=False)
    group_name = Column(String(60), nullable=False)
    active = Column(Integer, nullable=False, server_default=text("1"))


class SystemUser(Base):
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

    parent = relationship('SystemUser', remote_side=[user_id], primaryjoin='SystemUser.created_by == SystemUser.user_id')
    parent1 = relationship('SystemUser', remote_side=[user_id], primaryjoin='SystemUser.modified_by == SystemUser.user_id')


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

    system_user = relationship('SystemUser', primaryjoin='Organization.created_by == SystemUser.user_id')
    system_user1 = relationship('SystemUser', primaryjoin='Organization.modified_by == SystemUser.user_id')


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
