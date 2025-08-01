from hashlib import sha256
from flask import Flask, render_template, request, redirect, session, flash
from resources import db, User, login_manager, RegistrationForm, LoginForm, app
from flask_login import login_user, LoginManager, login_required, current_user

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=int(user_id)).first()

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST':
        for field in ['name', 'username', 'email', 'phone', 'password', 'password_confirm']:
            if not request.form[field]:
                return render_template('register.html', error_msg = f"Missing field '{field}'")
            
        if form.password.data == form.password_confirm.data:
            password_hash = sha256(form.password.data.encode()).hexdigest() #takes password that user provided and hashes it with sha256 returning hexadecimal value 
        else:
            return render_template('register.html', error_msg = "Passwords don't match")

        user = User(
            name = form.name.data,
            username = form.username.data,
            email = form.email.data,
            phone = form.phone.data,
            password_hash = password_hash
        )

        db.session.add(user)
        db.session.commit()
        return redirect('/')
    return render_template('register.html', form = form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/home')
    form = LoginForm()
    if request.method == 'POST':
        #data sent from login form
        if form.validate_on_submit():
            user = User.query.filter_by(username = form.username.data).first()
            if not user:
                return render_template('login.html', error_msg = 'User does not exist', form=form)
            if sha256(form.password.data.encode()).hexdigest() == user.password_hash:
                login_user(user)

            return redirect('/home') 
    return render_template('login.html', form=form)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/home')
@login_required
def home():
    return render_template('logged.html')