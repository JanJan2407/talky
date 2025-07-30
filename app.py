from hashlib import sha256
from flask import Flask, render_template, request, redirect
from resources import db, User
app = Flask(__name__)
# basicly create or open if already exists a database for storing user info
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
# initialize the app with the extension
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        for field in ['name', 'username', 'email', 'phone', 'pswrd', 'pswrdcnfrm']:
            if not request.form[field]:
                return render_template('register.html', error_msg = f"Missing field '{field}'")
            
        if request.form['pswrd'] == request.form['pswrdcnfrm']:
            password_hash = sha256(request.form['pswrd'].encode()).hexdigest() #takes password that user provided and hashes it with sha256 returning hexadecimal value 
        else:
            return render_template('register.html', error_msg = "Passwords don't match")

        user = User(
            name = request.form['name'],
            username = request.form['username'],
            email = request.form['email'],
            phone = request.form['phone'],
            password_hash = password_hash
        )
        db.session.add(user)
        db.session.commit()
        # TODO return redirect('/')
    return render_template('register.html')
  
@app.route('/')
def TODO():
    return render_template('index.html')