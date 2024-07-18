import os
from app import app, db
from models import Product, CartItem, Order, OrderItem

def seed_database():
    with app.app_context():
        db.create_all()  # Create tables if they don't exist

        try:
            # Clear existing cart items first (since they reference products)
            CartItem.query.delete()

            # Now delete products
            Product.query.delete()

            # Add sample products
            products = [
                Product(name='Car', description='Description for Car', price=909.99, stock_quantity=100, image_url='https://i.pinimg.com/474x/c0/b2/34/c0b234de7651f2e9de7c2a9578870909.jpg'),
                Product(name='Pen', description='Description for Pen', price=193.99, stock_quantity=50, image_url='https://www.pinterest.com/pin/746964288281587428/'),
                Product(name='House', description='Description for House', price=279.99, stock_quantity=20, image_url='https://i.pinimg.com/236x/23/78/bb/2378bb2b1e21fce6b3ae085cd462b121.jpg'),
                Product(name='Laptop', description='High-performance laptop', price=1200.00, stock_quantity=30, image_url='https://i.pinimg.com/474x/d3/eb/3e/d3eb3ee3d2d3afa4d6d2d130f0c3c21f.jpg'),
                Product(name='Notebook', description='Spiral notebook', price=5.99, stock_quantity=150, image_url='https://i.pinimg.com/564x/6f/0e/ef/6f0eef5a702b361c799bebcbf5e67999.jpg'),
                Product(name='Headphones', description='Noise-cancelling headphones', price=199.99, stock_quantity=75, image_url='https://i.pinimg.com/236x/07/7d/a6/077da67b6e52629d7092725956440be7.jpg')
            ]

            db.session.bulk_save_objects(products)  # Efficiently add multiple products
            db.session.commit()  # Commit the session

            # Add sample cart items (assuming product IDs correspond correctly)
            cart_items = [
                CartItem(product_id=1, quantity=2),  # Assuming product ID 1 exists
                CartItem(product_id=2, quantity=1)   # Assuming product ID 2 exists
            ]

            db.session.bulk_save_objects(cart_items)  # Efficiently add multiple cart items
            db.session.commit()  # Commit the session

            print("Database seeded with products and cart items!")

        except Exception as e:
            db.session.rollback()
            print(f"Error seeding database: {e}")

if __name__ == '__main__':
    seed_database()
