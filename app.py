import os
from dotenv import load_dotenv
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, Product, CartItem

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')  # Load database URL from environment
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize CORS
CORS(app)

# 
db.init_app(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Configure logging
if not app.debug:
    handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    )
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)

@app.route('/products', methods=['GET'])
def get_products():
    try:
        products = Product.query.all()
        product_list = [
            {
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'price': product.price,
                'stock_quantity': product.stock_quantity,
                'image_url': product.image_url
            }
            for product in products
        ]
        return jsonify({'products': product_list})
    except Exception as e:
        app.logger.error(f"Error fetching products: {e}")
        return jsonify({'message': 'Error fetching products'}), 500

@app.route('/cart', methods=['GET'])
def get_cart_items():
    try:
        cart_items = CartItem.query.all()
        cart_items_list = [
            {
                'id': item.id,
                'product_id': item.product_id,
                'quantity': item.quantity,
                'product': {
                    'name': item.product.name,
                    'price': item.product.price,
                    'image_url': item.product.image_url
                }
            }
            for item in cart_items
        ]
        return jsonify({'cart_items': cart_items_list})
    except Exception as e:
        app.logger.error(f"Error fetching cart items: {e}")
        return jsonify({'message': 'Error fetching cart items'}), 500

@app.route('/cart/add', methods=['POST'])
def add_to_cart():
    try:
        data = request.get_json()
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)  # Default quantity is 1 if not provided

        product = Product.query.get(product_id)
        if product and product.stock_quantity >= quantity:
            cart_item = CartItem.query.filter_by(product_id=product_id).first()
            if cart_item:
                cart_item.quantity += quantity
            else:
                cart_item = CartItem(product_id=product_id, quantity=quantity)
                db.session.add(cart_item)

            product.stock_quantity -= quantity
            db.session.commit()
            return jsonify({'message': 'Item added to cart successfully!'})
        else:
            return jsonify({'message': 'Item is out of stock or does not exist!'}), 400
    except Exception as e:
        app.logger.error(f"Error adding item to cart: {e}")
        return jsonify({'message': 'Error adding item to cart'}), 500

@app.route('/cart/remove/<int:cart_item_id>', methods=['DELETE'])
def remove_from_cart(cart_item_id):
    try:
        cart_item = CartItem.query.get(cart_item_id)
        if cart_item:
            product = Product.query.get(cart_item.product_id)
            product.stock_quantity += cart_item.quantity
            db.session.delete(cart_item)
            db.session.commit()
            return jsonify({'message': 'Item removed from cart successfully!'})
        else:
            return jsonify({'message': 'Cart item not found!'}), 404
    except Exception as e:
        app.logger.error(f"Error removing item from cart: {e}")
        return jsonify({'message': 'Error removing item from cart'}), 500

if __name__ == '__main__':
    app.run(debug=True)