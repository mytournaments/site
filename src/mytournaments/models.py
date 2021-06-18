from mytournaments import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    profile_picture = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    
    created_tournaments = db.relationship('Tournament', backref='author')

    def __repr__(self):
        return f'User({self.id!r}, {self.username!r}, {self.email!r})'


class Tournament(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    title = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.Text)
    game = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'Tournament({self.id!r}, {self.title!r}, {self.game!r})'
