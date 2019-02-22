from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, optional
from application.models import User

class LoginForms(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Register', render_kw={'class':'btn btn-primary'})

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
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
    item = StringField('New Item:', validators=[DataRequired()])
    quantity = SelectField('Quantity:', choices=[(1,1), (2,2), (3,3), (4,4), (5,5), (6,6), (7,7), (8,8), (9,9), (10,10)], coerce=int, default=1)

class Modify_item(FlaskForm):
    item = StringField('Item', validators=[DataRequired()])
    quantity = SelectField('Quantity:', choices=[(1,1), (2,2), (3,3), (4,4), (5,5), (6,6), (7,7), (8,8), (9,9), (10,10)], coerce=int, default=1)
    submit = SubmitField('Update', render_kw={'class':'btn btn-primary btn-xs'})