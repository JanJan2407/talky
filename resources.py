import json
import os 
from pathlib import Path

from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_login import LoginManager
from flask_moment import Moment

from helpers import get_date
from keys import key

app = Flask(__name__)

here = os.getcwd() # Gets current working directory
POST_UPLOAD_FOLDER = f'{here}/instance/post_images/' # Folder where uploaded images will be stored
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'} 
Path(POST_UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True) # Whenever app starts if folder doesn't exist it creates it

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db" # Configures database and names it users
app.config['POST_UPLOAD_FOLDER'] = POST_UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1000 * 1000 # Max img size is 50MB

app.secret_key = key # This is a private secret key 
moment = Moment(app)
db = SQLAlchemy(app)

app.jinja_env.globals.update(get_date = get_date) # Adds get_date from helpers to app so I can use it with Jinja2 on page load
app.jinja_env.globals.update(loads = json.loads) 

from models import *
# Create or open a database with columns for User
with app.app_context():
    db.create_all()

login_manager = LoginManager(app) # Configures app to use LoginManager to have all features that it provides
