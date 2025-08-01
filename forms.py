'''Structures of forms used on the website'''

from wtforms import StringField, EmailField, PasswordField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired

class RegistrationForm(FlaskForm):
    name         = StringField('name', validators=[DataRequired()])
    username     = StringField('username', validators=[DataRequired()])
    email        = EmailField('email', validators=[DataRequired()])
    phone        = StringField('phone', validators=[DataRequired()])
    password     = PasswordField('password', validators=[DataRequired()])
    password_confirm   = PasswordField('password_confirm', validators=[DataRequired()])

class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    