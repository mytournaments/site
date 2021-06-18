import os
from PIL import Image
from secrets import token_hex
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from mytournaments.forms import RegistrationForm, LoginForm, UpdateAccountForm, TournamentForm
from mytournaments.models import User, Tournament
from mytournaments import app, db, bcrypt


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=('GET', 'POST'))
def register():
    if current_user.is_authenticated:
        flash('You have already logged in.', 'warning')

        return redirect(url_for('index'))
    
    form = RegistrationForm()

    if form.validate_on_submit():
        
        filename = 'default.jpg'

        if form.profile_picture.data:
            token = token_hex(8)
            _, extension = os.path.splitext(form.profile_picture.data.filename)
            filename = token + extension
            path = os.path.join(app.root_path, 'static/img/pfps', filename)

            image = Image.open(form.profile_picture.data)
            image.thumbnail((128, 128))
            image.save(path)

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, profile_picture=filename)
        db.session.add(user)
        db.session.commit()

        flash('Your account has been created!', 'success')

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

    flash('You have successfully logged out.', 'success')

    return redirect(url_for('login'))


@app.route('/account', methods=('GET', 'POST'))
@login_required
def account():
    form = UpdateAccountForm()

    if form.validate_on_submit():
        if current_user.email == form.email.data and current_user.username == form.username.data and not form.profile_picture.data:
            flash('Both username, password and profile picture were the same as before.', 'warning')

            return redirect(url_for('account'))

        if form.profile_picture.data:
            token = token_hex(8)
            _, extension = os.path.splitext(form.profile_picture.data.filename)
            filename = token + extension
            path = os.path.join(app.root_path, 'static/img/pfps', filename)

            image = Image.open(form.profile_picture.data)
            image.thumbnail((128, 128))
            image.save(path)

            current_user.profile_picture = filename

        current_user.email = form.email.data
        current_user.username = form.username.data
        
        db.session.commit()

        flash('Your account has been updated.', 'success')

        return redirect(url_for('account'))
    
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.username.data = current_user.username

    return render_template('account.html', form=form)


@app.route('/create-tournament', methods=('GET', 'POST'))
@login_required
def create_tournament():
    form = TournamentForm()

    if form.validate_on_submit():
        tournament = Tournament(author=current_user, title=form.title.data, description=form.description.data, game=form.game.data)
        db.session.add(tournament)
        db.session.commit()

        flash('You have successfully created a new tournament.', 'success')
        
        return redirect(url_for('account'))

    return render_template('create-tournament.html', form=form)


@app.route('/tournaments')
def tournaments():
    return render_template('tournaments.html', tournaments=Tournament.query.all())
