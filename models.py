from sqlalchemy.orm import Mapped, mapped_column #used in User
from flask_login import  UserMixin
from wtforms import StringField, EmailField, PasswordField
from resources import db
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired

class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str]
    email: Mapped[str]
    phone: Mapped[str]
    password_hash: Mapped[str]

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
    