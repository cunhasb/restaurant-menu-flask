from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
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

# API's Endpoints (GET request only)


@app.route('/restaurants/JSON')
def restaurantsJSON():
    restaurants = session.query(Restaurant).all()
    return jsonify(Restaurants=[i.serialize for i in restaurants])


@app.route('/')
@app.route('/restaurants')
def showRestaurants():
    restaurants = session.query(Restaurant).all()
    # this page will show all my restaurants
    return render_template('restaurants.html', restaurants=restaurants)


@app.route('/restaurant/new', methods=['GET', 'POST'])
def newRestaurant():
    # this page will be for making a new restaurant
    if request.method == 'POST':
        newItem = Restaurant(
            name=request.form['name'])
        session.add(newItem)
        session.commit()
        flash('The %s Restaurant was sucessfully created!' %
              request.form['name'])
        return redirect(url_for('newRestaurant'))
    else:
        return render_template('newRestaurant.html')


@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    # pdb.set_trace()
    if request.method == 'POST':
        # pdb.set_trace()
        restaurant = session.query(
            Restaurant).filter_by(id=restaurant_id).one()
        restaurant.name = request.form['name']
        session.add(restaurant)
        session.commit()
        flash('The %s Restaurant was sucessfully updated!' % restaurant.name)
        return redirect(url_for('editRestaurant', restaurant_id=restaurant.id))
    else:
        # pdb.set_trace()
        restaurant = session.query(
            Restaurant).filter_by(id=restaurant_id).one()
        # this page will be for editing restaurant
        return render_template('editRestaurant.html', restaurant=restaurant)


@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    # this page will be for deleting restaurant
    if request.method == 'POST':
        restaurant = session.query(
            Restaurant).filter_by(id=restaurant_id).one()
        menuItems = session.query(MenuItem).filter_by(
            restaurant_id=restaurant_id).all()

        session.delete(restaurant)
        session.commit()
        flash('The %s Restaurant was successfully deleted!' % restaurant.name)
        return redirect(url_for('showRestaurants'))
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    return render_template('deleteRestaurant.html', restaurant=restaurant)


@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
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


@app.route('/restaurant/<int:restaurant_id>/menu/new/', methods=['GET', 'POST'])
def addMenuItem(restaurant_id):
    # this page will be for adding new menu items for menu
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        course = request.form['course']
        newItem = MenuItem(
            name=name, description=description, price=price, course=course, restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        flash('%s was sucessfully added to the menu!' %
              name)
        return redirect(url_for('addMenuItem', restaurant_id=restaurant_id))
    else:

        restaurant = session.query(
            Restaurant).filter_by(id=restaurant_id).one()
        return render_template('newMenuItem.html', restaurant=restaurant)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menuItem_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menuItem_id):
    # this page will be for editing menu items for restaurant
    if request.method == "POST":
        menuItem = session.query(MenuItem).filter_by(id=menuItem_id).one()
        menuItem.name = request.form['name']
        menuItem.description = request.form['description']
        menuItem.price = request.form['price']
        menuItem.course = request.form['course']
        session.add(menuItem)
        session.commit()
        flash('%s menu item was sucessfully updated!' % request.form['name'])
        return redirect(url_for('editMenuItem', restaurant_id=restaurant_id,
                                menuItem_id=menuItem_id))
    else:
        restaurant = session.query(
            Restaurant).filter_by(id=restaurant_id).one()
        menuItem = session.query(MenuItem).filter_by(id=menuItem_id).one()
        return render_template('editMenuItem.html', restaurant=restaurant, item=menuItem)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menuItem_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menuItem_id):
    # this page will be for deleting Menu Items
    if request.method == 'POST':
        menuItem = session.query(MenuItem).filter_by(id=menuItem_id).one()
        session.delete(menuItem)
        session.commit()
        flash('%s menu item was sucessfully deleted!' % menuItem.name)
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        restaurant = session.query(
            Restaurant).filter_by(id=restaurant_id).one()
        menuItem = session.query(MenuItem).filter_by(id=menuItem_id).one()
        return render_template('deleteMenuItem.html', restaurant=restaurant, menuItem=menuItem)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run("", port=3000)
