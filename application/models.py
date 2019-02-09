from datetime import datetime
from application import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('ShoppingItems', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

class ShoppingItems(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(64), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    added_to_chart = db.Column(db.Boolean, default=False, unique=False)
    quantity = db.Column(db.Integer, default=1, primary_key=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Item {}, Quantity {}, added to chart? {}>'.format(self.item, self.quantity, self.added_to_chart)

