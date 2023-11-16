from . import api
from ..models import db, Product, User, Cart
from flask import request, redirect

@api.get('/products')
def all_products_api():
    products = Product.query.all()
    products = [p.to_dict() for p in products]
    return {
        'status':'ok',
        'total_results': len(products),
        'products': products
    }

@api.get('/product/<product_id>')
def single_product_api(product_id):
    product = Product.query.get(product_id)
    if product:
        return {
            'status': 'ok',
            'total_results': 1, 
            'product': product.to_dict()
        }
    return {
        'status': 'not ok',
        'message': ' A post with that ID does not exist'
    }

@api.post('/user/create')
def create_user():
    data = request.json
    username = data['username']
    email = data['email']
    password = data['password']

    user = User.query.filter_by(username=username).first()
    if user:
        return {
            'status': 'not ok',
            'message': 'that username is already taken'
        }, 400
    
    user = User.query.filter_by(email=email).first()
    if user:
        return {
            'status': 'not ok',
            'message': 'that email is already taken'
        }, 400

    user = User(username, email, password)

    db.session.add(user)
    db.session.commit()

    return {
        'status': 'ok',
        "message": 'Successfully created your account!'
    }, 201



@api.post('/user/login')
def login():
    data = request.json
    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username).first()
    if not user:
        return {
            'status': 'not ok',
            'message': 'invalid username or password!'
        }, 400

    if user.password != password:
        return {
            'status': 'not ok',
            'message': 'invalid username or password'
        }, 400

    if user:
        return {
            'status': 'ok',
            'message': 'successfully logged in',
            'user': user.to_dict()
        }, 200
    
@api.post('/add-to-cart')
#login required
def addToCart(product_id):
    user = User.query.get(user_id)
    product = Product.query.get(product_id)
    user.cart.append(product)
    return {
        'status': 'ok',
        'message': 'added item to cart',
        'cart': [] + product
    }


@api.post('/delete-cart/<cart_id>')
#login required
def delete_cart(cart_id):
    cart = Cart.query.get(cart_id).all()
    cart = []
    db.session.commit()
    return {
        'status': 'ok',
        'message': 'removed everything from cart',
        'cart': cart
    }


@api.post('/remove/<product_id>')
#login required
def remove_from_cart(product_id):
   pass

@api.get('/my-cart/<cart_id>')
def my_cart(cart_id):
    cart = Cart.query.filter_by(cart_id).first()
    return {
        'status': 'ok',
        'message': 'heres your cart',
        'cart': cart.to_dict()
    }

import stripe
import os
stripe.api_key = os.environ.get('STRIPE_API_KEY')
FRONTEND_URL = 'http://localhost:5173/'

@api.post('/checkout')
def stripe_checkout():
    try:
        line_items=[]
        for price, qty in request.form.items():
            line_items.append({
                'price': price,
                'quantity': qty
            })
        checkout_session = stripe.checkout.Session.create(
            line_items=line_items,
            mode='payment',
            success_url=FRONTEND_URL + '?payment=seccess',
            cancel_url=FRONTEND_URL + '?payment=cancel',
        )
    except Exception as e:
        return str(e)
    
    return redirect(checkout_session.url, code=303)