from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, optional
from application.models import User

class LoginForms(FlaskForm):
    email = StringField('Email', validators=[DataRequired()], render_kw={'placeholder':'Enter Email Address'})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={'placeholder':'Enter Password'})
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login', render_kw={'class':'btn btn-primary'})

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], render_kw={'placeholder':'Username'})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={'placeholder':'Email Address'})
    password = PasswordField('Password', validators=[DataRequired()],render_kw={'placeholder':'Password'})
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')], render_kw={'placeholder':'Confirm Password'})
    submit = SubmitField('Register', render_kw={'class':'btn btn-primary'})

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username already taken')
    
    def validate_email(self, email):
        u = User.query.filter_by(email=email.data).first()
        if u is not None:
            raise ValidationError('Account with that email address is already created')

class Add_Item_Form(FlaskForm):
    item = StringField('New Item:', validators=[DataRequired()], render_kw={'placeholder':'Enter Item'})
    quantity = SelectField('Quantity:', choices=[(1,1), (2,2), (3,3), (4,4), (5,5), (6,6), (7,7), (8,8), (9,9), (10,10)], coerce=int, default=1)

class Modify_item(FlaskForm):
    item = StringField('Item', validators=[DataRequired()], render_kw={'class':'text-center'})
    quantity = SelectField('Quantity:', choices=[(1,1), (2,2), (3,3), (4,4), (5,5), (6,6), (7,7), (8,8), (9,9), (10,10)], coerce=int)
    submit = SubmitField('Update', render_kw={'class':'btn btn-primary btn-xs'})

class RequestPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={'placeholder':'Enter Email'})
    submit = SubmitField('Request New Password', render_kw={'class':'btn btn-primary'})

class Reset_PasswordForm(FlaskForm):
    password = StringField('Password', validators=[DataRequired()])
    password2 = StringField('Verify Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password', render_kw={'class':'btn btn-primary'})