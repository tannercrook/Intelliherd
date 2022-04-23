import sqlalchemy
import psycopg2
import models
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
from models.objects import PaymentType, Base, metadata



engine = create_engine("postgresql+psycopg2://tannercrook:Kinger413!@meridia.crooktec.com/intelliherd")
engine.connect()

session = scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=engine))
Base.query = session.query_property()

print(PaymentType.query.all())



