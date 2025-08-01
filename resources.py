from flask_sqlalchemy import SQLAlchemy
from keys import key
from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db" # Configures database and names it users
app.secret_key = key # This is a private secret key 

db = SQLAlchemy(app)

from models import User
# Create or open a database with Colums for User
with app.app_context():
    db.create_all()

login_manager = LoginManager(app) # Configures app to use loginmanager to have all features that it provides
