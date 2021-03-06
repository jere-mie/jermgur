from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, FileField, DecimalField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, NumberRange
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
    public = BooleanField("Is This Image Public?")
    content = TextAreaField('Content', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired(), Length(min=5, max=50)])
    price = DecimalField('Price (If For Sale)', validators=[DataRequired(), NumberRange(min=0.0)])
    forSale = BooleanField('Is This Image For Sale?')
    submit = SubmitField('Post')

class EditForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=5, max=50)])
    public = BooleanField("Is This Image Public?")
    content = TextAreaField('Content', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired(), Length(min=5, max=50)])
    price = DecimalField('Price (If For Sale)', validators=[DataRequired(), NumberRange(min=0.0)])
    forSale = BooleanField('Is This Image For Sale?')
    submit = SubmitField('Post')


class ReplyForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=5, max=50)])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')
