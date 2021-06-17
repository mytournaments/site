from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateTimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from mytournaments.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)], render_kw={'placeholder': 'Enter Username'})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={'placeholder': 'Enter Email'})
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)], render_kw={'placeholder': 'Enter Password'})
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')], render_kw={'placeholder': 'Confirm Password'})
    submit = SubmitField('Register')

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('That email is taken. Please choose a different one.')
    
    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError('That username is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={'placeholder': 'Enter Email'})
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)], render_kw={'placeholder': 'Enter Password'})
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class TournamentForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=30)], render_kw={'placeholder': 'Enter Title'})
    description = StringField('Description', validators=[DataRequired(), Length(max=700)], render_kw={'placeholder': 'Enter Description'})
    game = StringField('Game', validators=[DataRequired(), Length(max=20)], render_kw={'placeholder': 'Enter Game'})
    # start_date = DateTimeField('Date & Time', validators=[DataRequired()])
    submit = SubmitField('Create Tournament')
