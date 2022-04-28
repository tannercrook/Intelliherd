from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session, query
from models.objects import SystemUser, Base, metadata

import config.database_auth as dbauth


engine = create_engine("postgresql+psycopg2://{}:{}@{}/{}".format(dbauth.username,dbauth.password,dbauth.host,dbauth.database), implicit_returning=True)
engine.connect()

db_session = scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=engine))
Base.query = db_session.query_property()