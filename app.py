from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_security import Security, login_required, SQLAlchemySessionUserDatastore
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.database import db_session, init_db
from db.models import Base, Restaurant, MenuItem, User, Role
import pdb

# Create app
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'super_secret_key'
app.config['SECURITY_PASSWORD_SALT'] = 'super_secret_password_salt'
app.config['SECURITY_REGISTERABLE'] = True


# Setup Flask-Security
user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)
security = Security(app, user_datastore)


# Create a user to test with


@app.before_first_request
def create_user():
    init_db()
    # user_datastore.create_user(
    #     email='fabianocunhadev@gmail.com', password='password')
    # db_session.commit()


# Views
# API's Endpoints (GET request only)


@app.route('/restaurants/JSON/')
def restaurantsJSON():
    restaurants = db_session.query(Restaurant).all()
    return jsonify(Restaurants=[i.serialize for i in restaurants])


@app.route('/restaurant/<int:restaurant_id>/menu/JSON/')
@login_required
def restaurantMenuJSON(restaurant_id):
    restaurant = db_session.query(Restaurant).filter_by(id=restaurant_id)
    menuItems = db_session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).all()
    return jsonify(Restaurant=[i.serialize for i in restaurant], MenuItems=[i.serialize for i in menuItems])


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menuItem_id>/JSON/')
@login_required
def restaurantMenuItemJSON(restaurant_id, menuItem_id):
    restaurant = db_session.query(Restaurant).filter_by(id=restaurant_id)
    menuItem = db_session.query(MenuItem).filter_by(id=menuItem_id)
    return jsonify(Restaurant=[i.serialize for i in restaurant], MenuItem=[i.serialize for i in menuItem])


@app.route('/')
@app.route('/restaurants')
def showRestaurants():
    restaurants = db_session.query(Restaurant).all()
    # this page will show all my restaurants
    return render_template('restaurants.html', restaurants=restaurants)


@app.route('/restaurant/new', methods=['GET', 'POST'])
@login_required
def newRestaurant():
    # this page will be for making a new restaurant
    if request.method == 'POST':
        newItem = Restaurant(
            name=request.form['name'])
        db_session.add(newItem)
        db_session.commit()
        flash('The %s Restaurant was sucessfully created!' %
              request.form['name'])
        return redirect(url_for('newRestaurant'))
    else:
        return render_template('newRestaurant.html')


@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
@login_required
def editRestaurant(restaurant_id):
    # pdb.set_trace()
    if request.method == 'POST':
        # pdb.set_trace()
        restaurant = db_session.query(
            Restaurant).filter_by(id=restaurant_id).one()
        restaurant.name = request.form['name']
        db_session.add(restaurant)
        db_session.commit()
        flash('The %s Restaurant was sucessfully updated!' % restaurant.name)
        return redirect(url_for('editRestaurant', restaurant_id=restaurant.id))
    else:
        # pdb.set_trace()
        restaurant = db_session.query(
            Restaurant).filter_by(id=restaurant_id).one()
        # this page will be for editing restaurant
        return render_template('editRestaurant.html', restaurant=restaurant)


@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
@login_required
def deleteRestaurant(restaurant_id):
    # this page will be for deleting restaurant
    if request.method == 'POST':
        restaurant = db_session.query(
            Restaurant).filter_by(id=restaurant_id).one()
        menuItems = db_session.query(MenuItem).filter_by(
            restaurant_id=restaurant_id).all()

        db_session.delete(restaurant)
        db_session.commit()
        flash('The %s Restaurant was successfully deleted!' % restaurant.name)
        return redirect(url_for('showRestaurants'))
    restaurant = db_session.query(Restaurant).filter_by(id=restaurant_id).one()
    return render_template('deleteRestaurant.html', restaurant=restaurant)


@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
@login_required
def showMenu(restaurant_id):
    # this page will be for showing restaurant %s menu
    restaurant = db_session.query(Restaurant).filter_by(id=restaurant_id).one()
    menuItems = db_session.query(MenuItem).filter_by(
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
@login_required
def addMenuItem(restaurant_id):
    # this page will be for adding new menu items for menu
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        course = request.form['course']
        newItem = MenuItem(
            name=name, description=description, price=price, course=course, restaurant_id=restaurant_id)
        db_session.add(newItem)
        db_session.commit()
        flash('%s was sucessfully added to the menu!' %
              name)
        return redirect(url_for('addMenuItem', restaurant_id=restaurant_id))
    else:

        restaurant = db_session.query(
            Restaurant).filter_by(id=restaurant_id).one()
        return render_template('newMenuItem.html', restaurant=restaurant)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menuItem_id>/edit/', methods=['GET', 'POST'])
@login_required
def editMenuItem(restaurant_id, menuItem_id):
    # this page will be for editing menu items for restaurant
    if request.method == "POST":
        menuItem = db_session.query(MenuItem).filter_by(id=menuItem_id).one()
        menuItem.name = request.form['name']
        menuItem.description = request.form['description']
        menuItem.price = request.form['price']
        menuItem.course = request.form['course']
        db_session.add(menuItem)
        db_session.commit()
        flash('%s menu item was sucessfully updated!' % request.form['name'])
        return redirect(url_for('editMenuItem', restaurant_id=restaurant_id,
                                menuItem_id=menuItem_id))
    else:
        restaurant = db_session.query(
            Restaurant).filter_by(id=restaurant_id).one()
        menuItem = db_session.query(MenuItem).filter_by(id=menuItem_id).one()
        return render_template('editMenuItem.html', restaurant=restaurant, item=menuItem)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menuItem_id>/delete/', methods=['GET', 'POST'])
@login_required
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
    app.run("", port=3000)
