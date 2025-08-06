'''Structures of forms used on the website'''

from wtforms import StringField, EmailField, PasswordField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from flask_wtf.file import FileField


class RegistrationForm(FlaskForm):
    name = StringField('name', validators = [DataRequired()])
    username = StringField('username', validators = [DataRequired()])
    email = EmailField('email', validators = [DataRequired()])
    phone = StringField('phone', validators = [DataRequired()])
    password = PasswordField('password', validators = [DataRequired()])
    password_confirm = PasswordField('password_confirm', validators = [DataRequired()])

class LoginForm(FlaskForm):
    username = StringField('username', validators = [DataRequired()])
    password = PasswordField('password', validators = [DataRequired()])
    
class PostForm(FlaskForm):
    username = StringField('username', validators = [DataRequired()]) # Username of the person who posted the post
    title = StringField('title', validators = [DataRequired()])
    post_content = StringField('post_content', validators = [DataRequired()])
    image = FileField('image') # I wanted to use FileAllowed but it for some reason didn't work so I check this a bit later now with help of py fun

class CommentForm(FlaskForm):
    comment = StringField('comment', validators = [DataRequired()])