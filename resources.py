from flask_sqlalchemy import SQLAlchemy
from keys import key
from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)
# basicly create or open if already exists a database for storing user info

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.secret_key = key

db = SQLAlchemy(app)

from models import User, LoginForm, RegistrationForm

with app.app_context():
    db.create_all()

login_manager = LoginManager(app)

