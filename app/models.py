from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    my_cart = db.relationship("Cart", backref='my_cart')



    def __init__(self, first_name, username, email, password):
        self.first_name = first_name
        self.username = username
        self.email = email
        self.password = password
    


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    img_url = db.Column(db.String, nullable=False)
    description = db.Column(db.String(500))
    price = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)

    in_cart = db.relationship("Cart", backref='in_cart')

    def __init__(self, title, img_url, description, price):
        self.title = title
        self.img_url = img_url
        self.description = description
        self.price = price


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    total = db.Column(db.String)

    def __init__(self, user_id, product_id, total):
        self.user_id = user_id
        self.product_id = product_id
        self.total = total 


    def get_cart(self):
        my_cart = {p.id for p in self.cart}
        return my_cart
    
    
    def cart_total(self):
        return sum(self.product_price)
    
        
    def to_dict(self):
        return {
            'title': self.product.title,
            'description': self.product.description,
            'img_url': self.product.img_url,
            'user_id': self.user_id,
            'date_created': self.date_created,
            'last_updated': self.last_updated,
            'total': self.cart_total()
        }
    
