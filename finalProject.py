from flask import Flask
app = Flask(__name__)


@app.route('/')
@app.route('/restaurants')
def showRestaurants():
    return 'this page will show all my restaurants'


@app.route('/restaurant/new')
def newRestaurant():
    return 'this page will be for making a new restaurant'


@app.route('/restaurant/<int:restaurant_id>/edit')
def editRestaurant(restaurant_id):
    return 'this page will be for editing restaurant %s' % restaurant_id


@app.route('/restaurant/<int:restaurant_id>/delete')
def deleteRestaurant(restaurant_id):
    return 'this page will be for deleting restaurant %s' % restaurant_id


@app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    return 'this page will be for showing restaurant %s menu' % restaurant_id


@app.route('/restaurant/<int:restaurant_id>/menu/new')
def addMenuItem(restaurant_id):
    return 'this page will be for adding new menu items for menu %s' % restaurant_id


@app.route('/restaurant/<int:restaurant_id>/menu/edit')
def editMenuItem(restaurant_id):
    return 'this page will be for editing menu items for restaurant %s' % restaurant_id


@app.route('/restaurant/<int:restaurant_id>/menu/delete')
def deleteMenuItem(restaurant_id):
    return 'this page will be for deleting menu items for restaurant %s' % restaurant_id


if __name__ == '__main__':
    app.debug = True
    app.run("", port=3000)
