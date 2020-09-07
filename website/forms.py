from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, FileField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from website.models import User, Post
from website import db


class Register(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=20)])    
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5, max=20)])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken')


class Login(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    rememberMe = BooleanField('Remember Me')
    submit = SubmitField('Sign In')  



class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=5, max=50)])
    image = FileField('Upload Image', validators=[DataRequired()])
    public = BooleanField("Public?")
    # content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')


    # id = db.Column(db.Integer, primary_key=True)
    # title = db.Column(db.String(100), nullable=False)
    # date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # image = db.Column(db.String(100), unique=True)
    # content = db.Column(db.Text, nullable=False)
    # public = db.Column(db.Boolean, default=True, nullable=False)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # replies = db.relationship('Reply', backref='original', lazy=True)