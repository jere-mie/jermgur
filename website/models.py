from datetime import datetime
from enum import unique
from website import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    replies = db.relationship('Reply', backref='writer', lazy=True)
    money = db.Column(db.Float, default=100.0, nullable=False)

    def __repr__(self):
        return f"Username: {self.username}"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    anonid = db.Column(db.String(12), nullable=False, unique=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    image = db.Column(db.String(100), unique=True)
    content = db.Column(db.Text, nullable=False)
    public = db.Column(db.Boolean, default=True, nullable=False)
    forSale = db.Column(db.Boolean, default=False, nullable=False)
    price = db.Column(db.Float, default=0.0, nullable=False)
    discount = db.Column(db.Float, default=0.0, nullable=False)
    # relationships
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    replies = db.relationship('Reply', backref='original', lazy=True)

class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seller = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    buyer = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)


class Reply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
