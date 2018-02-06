from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
import pdb
app = Flask(__name__)
engine = create_engine(
    'postgresql://restaurant:restaurantPassword@localhost:5432/restaurant')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/restaurants')
def showRestaurants():
    restaurants = session.query(Restaurant).all()
    # this page will show all my restaurants
    return render_template('restaurants.html', restaurants=restaurants)


@app.route('/restaurant/new')
def newRestaurant():
    # this page will be for making a new restaurant
    return render_template('newRestaurant.html')


@app.route('/restaurant/<int:restaurant_id>/edit')
def editRestaurant(restaurant_id):
    # pdb.set_trace()
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    # this page will be for editing restaurant
    return render_template('editRestaurant.html', restaurant=restaurant)


@app.route('/restaurant/<int:restaurant_id>/delete')
def deleteRestaurant(restaurant_id):
    # this page will be for deleting restaurant
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    return render_template('deleteRestaurant.html', restaurant=restaurant)


@app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    # this page will be for showing restaurant %s menu
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    menuItems = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).group_by('course', 'id').all()
    courses = []
    for el in menuItems:
        if el.course not in courses:
            courses.append(el.course)
    for el in courses:
        print(el)
    print (len(courses))
    # pdb.set_trace()
    return render_template('menuItems.html', restaurant=restaurant, menuItems=menuItems, courses=courses)


@app.route('/restaurant/<int:restaurant_id>/menu/new')
def addMenuItem(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    # this page will be for adding new menu items for menu
    return render_template('newMenuItem.html', restaurant=restaurant)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menuItem_id>/edit')
def editMenuItem(restaurant_id, menuItem_id):
    # this page will be for editing menu items for restaurant
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    menuItem = session.query(MenuItem).filter_by(id=menuItem_id).one()
    return render_template('editMenuItem.html', restaurant=restaurant, item=menuItem)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menuItem_id>/delete')
def deleteMenuItem(restaurant_id, menuItem_id):
    # this page will be for deleting Menu Items
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    menuItem = session.query(MenuItem).filter_by(id=menuItem_id).one()
    return render_template('deleteMenuItem.html', restaurant=restaurant, menuItem=menuItem)


if __name__ == '__main__':
    app.debug = True
    app.run("", port=3000)
