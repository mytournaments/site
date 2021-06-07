from flask import render_template, redirect, url_for, request
from flask_login import login_user, logout_user, login_required, current_user
from mytournaments.models import User
from mytournaments import app, db, bcrypt


@app.route('/')
def index():
    return '<h1>Hello World!</h1>'


@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')

        if all([username, password, email]):
            if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
                return '<h1>Username or email already used.</h1>'
            
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            user = User(username=username, email=email, password=hashed_password)
            db.session.add(user)
            db.session.commit()

            return redirect(url_for('login'))

        return '<h1>All fields are required.</h1>'

    return render_template('register.html')


@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=True)

            next_page = request.args.get('next')

            return redirect(next_page) if next_page is not None else redirect(url_for('dashboard'))
        
        return '<h1>Invalid credentials. Please try again.</h1>'
    
    return render_template('login.html')


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
