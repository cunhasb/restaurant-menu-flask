from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
from mimesis import Generic
import random

# Creates connection with database
engine = create_engine(
    'postgresql://restaurant:restaurantPassword@localhost:5432/restaurant')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()
courses = ['Appetizer', 'Soup', 'Fish', 'Salad', 'Main course', 'Dessert']
g = Generic('en')

# Create Restaurants

for i in range(0, 10):

    restaurant = Restaurant(name=g.business.company())
    session.add(restaurant)
    session.commit()


# Read and Print Restaurants

restaurants = session.query(Restaurant)
for restaurant in restaurants:
    print(restaurant.name)

# Create MenuItems

for restaurant in restaurants:
    for i in range(0, 15):
        item = MenuItem(name=g.food.dish(), description=g.text.text(5)[:250], price=g.business.price(
            minimum=1.99, maximum=50.0), course=courses[random.randint(0, len(courses) - 1)], restaurant_id=restaurant.id)
        session.add(item)
        session.commit()


# Read and Print  MenuItems

items = session.query(MenuItem)
for item in items:
    print(item.name, item.restaurant.id)

# close session and close connection

session.close()
engine.dispose()
