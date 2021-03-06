from datetime import datetime
from application import db, app, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import jwt
from time import time


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    count_logged_in = db.Column(db.Integer, primary_key=False)
    last_logged_on = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('ShoppingItems', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_hash(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_hash(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode({'reset_password':self.id, 'exp': time() + expires_in}, app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')
    
    def verify_reset_password_token(token):
        try:
            userid = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(userid)

class ShoppingItems(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(64), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    added_to_chart = db.Column(db.Boolean, default=False, unique=False)
    quantity = db.Column(db.Integer, default=1, primary_key=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Item {}, Quantity {}, added to chart? {}>'.format(self.item, self.quantity, self.added_to_chart)

#function is needed to keep track of logged in user, the ID that is passed in the function is a string 
@login.user_loader
def load_user(id):
    return User.query.get(int(id))



