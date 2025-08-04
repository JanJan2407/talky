from hashlib import sha256
import json # Java script object notation to help store comments on a post in 1 string 
import time
from datetime import datetime, UTC

from flask import render_template, request, redirect, url_for
from flask_login import login_user, login_required, current_user, logout_user

from resources import app, db, login_manager
from forms import LoginForm, RegistrationForm, PostForm, CommentForm
from models import User, Post
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
                return render_template('register.html', error_msg = f"Missing field '{field}'", form = form)
            
        if form.password.data == form.password_confirm.data:
            password_hash = sha256(form.password.data.encode()).hexdigest() # Takes password that user provided and hashes it with sha256 returning hexadecimal value 
        else:
            return render_template('register.html', error_msg = "Passwords don't match", form = form)

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


@app.route('/') # Not done yet currently displays progres
def index():
    return render_template('index.html')


@app.route('/users') # Display all users
def user_list():
    users = User.query.filter_by().all()
    return render_template('userlist.html', users = users)

@app.route('/posts') # Display all posts
def show_posts():
    posts = Post.query.filter_by().all()
    return render_template('posts.html', posts = posts)

@app.route('/view/<id>', methods = ['GET']) # Show specific post on whole page also displayes any comments on the post
def view(id):
    form = CommentForm()
    post = Post.query.filter_by(id = id).first()
    comments = json.loads(post.comments)
    return render_template('view.html', post = post, form = form, comments = comments)


@app.route('/view/post/<id>', methods = ['POST'])
@login_required # Logged in users can add coments to posts
def add_comment(id):
    comment_time = int(time.time())
    form = CommentForm()
    post = Post.query.filter_by(id = id).first()
    comment = form.comment.data
    username = current_user.username
    current_comments = json.loads(post.comments)
    comment_id = post.comment_id
    current_comments.append({'username': username, 'content': comment, 'id' : comment_id, 'time' : comment_time}) # Adds a comment
    post.comments = json.dumps(current_comments)
    post.comment_id += 1
    db.session.commit()
    return redirect(f'/view/{id}')


@app.route('/home')
@login_required
def hello():
    return render_template('logged.html')

@app.route('/post', methods = ['GET', 'POST'])
@login_required
def post(): # Allow users to post messages for everyone
    form = PostForm()
    if request.method == 'POST':
        current_time = time.time() # In seconds since epoch (Jan 1st 1970 UTC)
        username = current_user.username
        title = form.title.data
        post_content = form.post_content.data
        post = Post(
            username = username,
            title = title,
            post_content = post_content,
            time = current_time # In db value stored is not date yet it gets converted to users local time with jinja when page is loaded
        )
        db.session.add(post)
        db.session.commit()

    return render_template("post.html", form = form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')

@app.route("/remove/<int:post_id>", methods = ['POST']) # Removes a post
@app.route("/remove/<int:post_id>/<int:comment_id>", methods = ['POST']) # Removes a comment 
@login_required
def remove(post_id, comment_id = None):
    post = Post.query.filter_by(id = post_id).first()
    if comment_id != None: # Comment will be deleated 
        print("Here")
        comments = json.loads(post.comments)
        for i in range(len(comments)):
            if comments[i]['id'] == int(comment_id):
                comment = comments[i]
                comment_index = i
                break

        # Only if you are the commenter or the owner of the post
        if current_user.username == post.username or current_user.username == comment['username']:
            comments.pop(comment_index)
            post.comments = json.dumps(comments)
            db.session.commit()

        return redirect(f'/view/{ post_id }')
    
    elif current_user.username == post.username: # Post will be deleated
        db.session.delete(post)
        db.session.commit()
        return redirect('/posts')

    