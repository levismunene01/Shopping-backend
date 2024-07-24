import os
from app import app, db
from models import Product, CartItem, OrderItem

def seed_database():
    with app.app_context():
        db.create_all()  # Create tables if they don't exist

        try:
            # Clear existing cart items first (since they reference products)
            CartItem.query.delete()

            # Clear order items first (since they reference products)
            OrderItem.query.delete()

            # Now delete products
            Product.query.delete()

            # Add sample products
            products = [
                Product(
                    name='Oxford Shoes',
                    description='oxford shoes for men patent leather wedding shoes pointed',
                    price=90.99,
                    stock_quantity=100,
                    image_url='https://www.pinterest.com/pin/620933867389335509/'
                ),
                Product(
                    name='Highschool Bata',
                    description='Best school shoes',
                    price=43.99,
                    stock_quantity=50,
                    image_url='https://i.pinimg.com/236x/1d/da/f7/1ddaf7e6697c5d2923179d05d8773dcc.jpg'
                ),
                Product(
                    name='Bigtree women',
                    description='BIGTREE Shoes Women Pumps Fashion High Heels For Women Shoes Casual Pointed To',
                    price=79.99,
                    stock_quantity=20,
                    image_url='https://i.pinimg.com/236x/34/ad/47/34ad474e07590a747b743bcbc707362d.jpg'
                ),
                Product(
                    name='Jordar 1 low cut',
                    description='Nike womens Dunk Low',
                    price=120.00,
                    stock_quantity=30,
                    image_url='https://i.pinimg.com/474x/63/bf/34/63bf34fb0e26f1c9f2400285d54a34a4.jpg'
                ),
                Product(
                    name='Notebook',
                    description='Spiral notebook',
                    price=5.99,
                    stock_quantity=150,
                    image_url='https://i.pinimg.com/564x/6f/0e/ef/6f0eef5a702b361c799bebcbf5e67999.jpg'
                ),
                Product(
                    name='Jordan',
                    description='Cool Jordan 4 shoes',
                    price=199.99,
                    stock_quantity=75,
                    image_url='https://i.pinimg.com/236x/52/39/cc/5239cccd10c2d2e81cf21138235ba789.jpg'
                ),
                Product(
                    name='Jordan 24',
                    description='The latest shoes',
                    price=60.95,
                    stock_quantity=80,
                    image_url='https://i.pinimg.com/474x/0c/bc/c1/0cbcc1fb7dc5c1bcbb537af293fee9d8.jpg'
                )
            ]

            db.session.bulk_save_objects(products)  # Efficiently add multiple products
            db.session.commit()  # Commit the session

            print("Database seeded with products!")

        except Exception as e:
            db.session.rollback()
            print(f"Error seeding database: {e}")

if __name__ == '__main__':
    seed_database()
