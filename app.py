from hashlib import sha256

from flask import render_template, request, redirect, url_for
from flask_login import login_user, login_required, current_user, logout_user

from resources import app, db, login_manager
from forms import LoginForm, RegistrationForm
from models import User
from helpers import valid_error

# Loads the user if logged in
@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id = int(user_id)).first()

login_manager.session_protection = "strong"

# What happens when a user tries to access certain content without being logged in 
@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login', error = 'Please log in to access that'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form) # Defines the structure of the form 
    if request.method == 'POST':
        for field in ['name', 'username', 'email', 'phone', 'password', 'password_confirm']: # Checks that all input fields exist
            if not request.form[field]:
                return render_template('register.html', error_msg = f"Missing field '{field}'")
            
        if form.password.data == form.password_confirm.data:
            password_hash = sha256(form.password.data.encode()).hexdigest() # Takes password that user provided and hashes it with sha256 returning hexadecimal value 
        else:
            return render_template('register.html', error_msg = "Passwords don't match")

        user = User(
            name = form.name.data,
            username = form.username.data,
            email = form.email.data,
            phone = form.phone.data,
            password_hash = password_hash
        )
        # Tries to add user with it's data to db if username is already taken, is user notified 
        try:
            db.session.add(user)
            db.session.commit()
        except Exception:
            return render_template('register.html', form = form, error_msg = "Username already taken") # Every form=form just tells the page structure of the form it's neccecary for page to work

        return redirect('/')
    return render_template('register.html', form = form)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    error = request.args.get('error') # This error will only arrive if user tried accessing content login restricted

    if current_user.is_authenticated:
        return redirect('/home') # If already logged in
    
    form = LoginForm()

    if request.method == 'POST':
        # Validates if form was submitted correctly 
        if form.validate_on_submit():
            # If username provided and password provided match with data in db
            # Password in db is stored as has hso when we compare we convert to hash as well
            user = User.query.filter_by(username = form.username.data).first()
            if not user:
                return render_template('login.html', form = form, error_msg = 'Username does not exist')
            
            if sha256(form.password.data.encode()).hexdigest() == user.password_hash:
                login_user(user, remember=True) # Users session will be remembered even if they close the browser
                return redirect('/home')
            
            return render_template('login.html', form = form, error_msg = 'Incorrect password')
        
    if valid_error(error): # Checks if error message is allowed
        return render_template('login.html', form = form, error_msg = error)
    
    return render_template('login.html', form = form)


@app.route('/') # Not done yet currently displays progress
def index():
    return render_template('index.html')

@app.route('/home')
@login_required # Flask-login provided decorator that allows only logged in users to access
def home():
    return render_template('logged.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')