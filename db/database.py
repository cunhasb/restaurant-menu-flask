import os
import sys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine
import pdb

'''psql
postgres=# CREATE DATABASE restaurant;
CREATE DATABASE
postgres=# CREATE USER restaurant WITH PASSWORD 'restaurantPassword';
CREATE ROLE
postgres=# GRANT ALL PRIVILEGES ON DATABASE restaurant TO RESTAURANT;
GRANT'''


engine = create_engine(
    'postgresql://restaurant:restaurantPassword@localhost:5432/restaurant')
db_session = scoped_session(sessionmaker(
    autocommit=False, autoFlush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    '''import all modules here that might define models so that
    they will be registered properly on the metadata. Otherwise
    you will have to import them first before calling init_db()
    '''
    import models
    Base.metadata.create_all(bind=engine)


def connect(user, password, db, host='localhost', port=5432):
    '''Returns a connection and a metadata object'''
    # We connect with the help of the PostgreSQL URL
    # postgresql://RESTAURANT:restaurantPassword@localhost:5432/restaurant
    url = 'postgresql://{}:{}@{}:{}/{}'
    url = url.format(user, password, host, port, db)
