from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from mytournaments.forms import RegistrationForm, LoginForm
from mytournaments.models import User
from mytournaments import app, db, bcrypt


@app.route('/')
def index():
    return '<h1>Hello World!</h1>'


@app.route('/register', methods=('GET', 'POST'))
def register():
    if current_user.is_authenticated:
        flash('You have already logged in.', 'warning')

        return redirect(url_for('index'))
    
    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash('Your account has been created! You are now able to log in.', 'success')

        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=('GET', 'POST'))
def login():
    if current_user.is_authenticated:
        flash('You have already logged in.', 'warning')

        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')

            flash('You have logged in.', 'success')
            
            return redirect(next_page) if next_page else redirect(url_for('index'))
        
        else:
            flash('Login Unsuccessful. Please check email and password.', 'danger')

    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()

    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_authenticated:
        return f'<h1>Welcome back {current_user.username}!</h1>'
    
    return '<h1>You are not logged in.</h1>'
