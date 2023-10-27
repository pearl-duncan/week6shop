from app import app 
from flask import render_template, redirect, request, url_for, flash
from .forms import ProductForm
from .models import Product, db, Cart
from flask_login import current_user, login_required
from datetime import datetime


@app.route('/product/create', methods=['GET', 'POST'])
@login_required
def create_product():
    form = ProductForm()
    if request.method == 'POST':
        if form.validate():
            title = form.title.data
            img_url = form.img_url.data
            description = form.description.data
            price = form.price.data

            product = Product(title, img_url, description, price)
            
            db.session.add(product)
            db.session.commit()
            print('created product', product)
            flash('Successfully created a product!', 'success')

            return redirect(url_for('home'))
        
    return render_template('create-product.html', form=form)


@app.route('/')
def home():
    product = Product.query.all()
    return render_template('home.html', p=product)

@app.route('/addToCart')
def addToCart(product_id):
    product = Product.get(product_id)
    user = current_user.id
    cart = Cart(product, user)

    db.session.add(cart)
    db.session.commit()

    flash('Successfully created a product!', 'success')
    return redirect(url_for('cart'))



@app.route('/cart', methods=['GET', 'POST'])

@app.route('/product/<product_id>')
@login_required
def ind_product(product_id):
    product = Product.query.get(product_id)
    return render_template("ind-product.html", p=product)

@app.route('/product/update/<product_id>', methods=['GET', 'POST'])
@login_required
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        flash('That product does not exist', 'danger')
        return redirect(url_for('home'))
    if current_user.id != product.user_id:
        flash('You cannot edit another user\'s product', 'danger')
        return redirect(url_for('ind_product', product_id=product_id))
    form = ProductForm()
    if request.method == 'POST':
        if form.validate():
            title = form.title.data
            img_url = form.img_url.data
            description = form.description.data
            price = form.price.data

            product.title = title
            product.img_url = img_url
            product.description = description
            product.price = price
            product.last_updated = datetime.utcnow()

            db.session.commit()
            flash('Successfully updated your product', 'success')
            return redirect(url_for('ind_product', product_id=product_id))

    return render_template("update-product.html", p=product, form=form)


@app.route('/product/delete/<product_id>', methods=['GET', 'POST'])
@login_required
def delete_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        flash('That product does not exist', 'danger')
        return redirect(url_for('home'))
    if current_user.id != product.user_id:
        flash('You cannot delete another user\'s product', 'danger')
        return redirect(url_for('ind_post', product_id=product_id))

    db.session.delete(product)
    db.session.commit()
    flash('Successfully deleted your product!', 'success')
    return redirect(url_for('home'))


