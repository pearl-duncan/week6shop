from . import auth
from flask import render_template, redirect, request, url_for, flash
from .forms import SignUpForm, LoginForm
from ..models import User, db
from flask_login import login_user, logout_user, current_user, login_required

#@auth.route('/')
#def index():
#    return render_template('index.html')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if request.method == 'POST':
        flash("Form Submitted!", 'success')
        if form.validate():
            username = form.username.data
            email = form.email.data
            password = form.password.data

            user = User(username, email, password)

            db.session.add(user)
            db.session.commit()

            flash('Successfully creadted your accout. Login now.', 'success')
            return redirect(url_for('auth.login'))

        else:
            flash('Invalid form, please try again', 'danger')

    return render_template('signup.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
            return redirect(url_for('home'))
    form = LoginForm()
    if request.method == 'POST':
        if form.validate():
            username = form.username.data
            password = form.password.data

            user= User.query.filter_by(username=username).first()

            if user:
                if user.password == password:
                    login_user(user)
                    flash("Successfully logged in", 'success')
                    return redirect(url_for('home'))

                else:
                    flash("Invalid username or password!", 'danger')
            else:
                flash('That username does not exists.', 'danger')
    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


