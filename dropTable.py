import os
import sys
from sqlalchemy import create_engine, inspect, MetaData
import pdb

# To drop database in PostgreSQL
# irreversible,database cannot be in use by anyone.
# psql
# \list
# DROP DATABASE IF EXISTS name;


# Create engine and establish connection
engine = create_engine(
    'postgresql://restaurant:restaurantPassword@localhost:5432/restaurant')


# Inspect - Get Database information
inspector = inspect(engine)
print ('Tables', inspector.get_table_names())
print ('Restaurant - Colunns', inspector.get_columns('restaurant'))
print ('MenuItem - Colunns', inspector.get_columns('menu_item'))

# Reflection - Loading Table from Existing database_setup
# Creating MetaData instance

metadata = MetaData()
# reflect db schema to MetaData
metadata.reflect(bind=engine)
print (metadata.tables)

# bind in order to Drop
metadata._bind_to(engine)
metadata.drop_all()
engine.dispose()
