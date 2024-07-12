#!/usr/bin/env python3
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from models import db, Restaurant, Pizza, RestaurantPizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
    return jsonify([restaurant.to_dict(only=['id', 'name', 'address']) for restaurant in restaurants])

@app.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if restaurant is None:
        return jsonify({"error": "Restaurant not found"}), 404
    return jsonify(restaurant.to_dict())

@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if restaurant is None:
        return jsonify({"error": "Restaurant not found"}), 404
    db.session.delete(restaurant)
    db.session.commit()
    return '', 204

@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    pizzas = Pizza.query.all()
    return jsonify([pizza.to_dict(only=['id', 'name', 'ingredients']) for pizza in pizzas])

@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    data = request.get_json()
    price = data.get('price')
    if not RestaurantPizza.validate_price(price):
        return jsonify({"errors": ["Price must be between 1 and 30"]}), 400
    restaurant_pizza = RestaurantPizza(
        price=price,
        restaurant_id=data.get('restaurant_id'),
        pizza_id=data.get('pizza_id')
    )
    db.session.add(restaurant_pizza)
    db.session.commit()
    return jsonify(restaurant_pizza.to_dict()), 201

if __name__ == '__main__':
    app.run(debug=True, port=5555)