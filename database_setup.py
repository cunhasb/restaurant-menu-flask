import os
import sys
from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import pdb

'''psql
postgres=# CREATE DATABASE restaurant;
CREATE DATABASE
postgres=# CREATE USER restaurant WITH PASSWORD 'restaurantPassword';
CREATE ROLE
postgres=# GRANT ALL PRIVILEGES ON DATABASE restaurant TO RESTAURANT;
GRANT'''


Base = declarative_base()


def connect(user, password, db, host='localhost', port=5432):
    '''Returns a connection and a metadata object'''
    # We connect with the help of the PostgreSQL URL
    # postgresql://RESTAURANT:restaurantPassword@localhost:5432/restaurant
    url = 'postgresql://{}:{}@{}:{}/{}'
    url = url.format(user, password, host, port, db)


class Restaurant(Base):
    __tablename__ = 'restaurant'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)


class MenuItem(Base):
    __tablename__ = 'menu_item'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(String(250))
    price = Column(String(8))
    course = Column(String(250))
    restaurant_id = Column(Integer, ForeignKey(
        'restaurant.id', ondelete='CASCADE'))
    restaurant = relationship(
        Restaurant, single_parent=True)


# engine = create_engine(connect('restaurant', 'restaurantPassword', 'restaurant'))
engine = create_engine(
    'postgresql://restaurant:restaurantPassword@localhost:5432/restaurant')
Base.metadata.create_all(engine)
