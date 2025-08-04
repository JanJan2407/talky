from flask_sqlalchemy import SQLAlchemy
from keys import key
from flask import Flask
from flask_login import LoginManager
from flask_moment import Moment
from helpers import get_date
app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db" # Configures database and names it users
app.secret_key = key # This is a private secret key 
moment = Moment(app)
db = SQLAlchemy(app)
app.jinja_env.globals.update(get_date = get_date) # Adds get_date from helpers to app so I can use it with Jinja2 on page load


from models import *
# Create or open a database with Colums for User
with app.app_context():
    db.create_all()

login_manager = LoginManager(app) # Configures app to use loginmanager to have all features that it provides
