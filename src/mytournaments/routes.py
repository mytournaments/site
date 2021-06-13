from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from mytournaments.forms import RegistrationForm, LoginForm, TournamentForm
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
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
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
            flash('Login Unsuccessful. Please check email and password.', 'error')

    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()

    flash('You have successfully logged out.')

    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    return f'<h1>Welcome back {current_user.username}!</h1>'


@app.route('/create-tournament', methods=('GET', 'POST'))
@login_required
def create_tournament():
    form = TournamentForm()

    if form.validate_on_submit():
        tournament = Tournament(author=current_user, title=form.title.data, description=form.description.data, game=form.game.data)
        db.session.add(tournament)
        db.session.commit()

        flash('You have successfully created a new tournament.', 'success')
        
        return redirect(url_for('index'))

    return render_template('create-tournament.html', form=form)


@app.route('/tournaments')
def tournaments():
    return render_template('tournaments.html', tournaments=Tournament.query.all())
