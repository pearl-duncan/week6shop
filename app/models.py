from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    my_cart = db.relationship("Cart", backref='my_cart', cascade="all,delete-orphan")



    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def to_dict(self):
        return {
            'email': self.email,
            'username': self.username,
            'password': self.password
        }
        
    


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    img_url = db.Column(db.String, nullable=False)
    description = db.Column(db.String(500))
    price = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)

    in_cart = db.relationship("Cart", backref='in_cart', cascade="all,delete-orphan")


    def __init__(self, title, img_url, description, price):
        self.title = title
        self.img_url = img_url
        self.description = description
        self.price = price


    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'img_url': self.img_url,
            'description': self.description,
            'price': self.price,
            'date_created': self.date_created,
            'last_updated': self.last_updated
        }

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)



    def __init__(self, user_id, product_id):
        self.user_id = user_id
        self.product_id = product_id
   
    
        
    def to_dict(self):
        return {
            'products': self.products.to_dict(),
            'total': self.cart_total(),
            'owner': self.user_id
        }
    
