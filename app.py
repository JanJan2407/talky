from hashlib import sha256
import time
import os

from flask import render_template, request, redirect, url_for, send_from_directory
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.utils import secure_filename
from PIL import Image
from resources import app, db, login_manager
from forms import LoginForm, RegistrationForm, PostForm, CommentForm
from models import User, Post, Comment, Like
from helpers import valid_error, allowed_file

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
            return render_template('register.html', form = form, error_msg = "Username already taken") # Every form=form just tells the page structure of the form it's necessary for page to work

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


@app.route('/users') # Display all users
def user_list():
    users = User.query.filter_by().all()
    return render_template('userlist.html', users = users)

@app.route('/posts') # Display all posts
def show_posts():
    posts = Post.query.all()
    reactions = Like.query.filter_by(comment_id = None).all()  # Only post reactions

    # Build a dict: {post_id: {'likes': count, 'dislikes': count, 'liked_by': [...], 'disliked_by': [...]}}
    post_reactions = {}
    for post in posts:
        likes = [r.username for r in reactions if r.post_id == post.id and r.is_like] # Get usernames of users who liked the post
        dislikes = [r.username for r in reactions if r.post_id == post.id and not r.is_like] # Get usernames of users who disliked the post
        post_reactions[post.id] = {
            'like_count': len(likes),
            'dislike_count': len(dislikes),
            'liked_by': likes,
            'disliked_by': dislikes
        }

    return render_template('posts.html', posts=posts, post_reactions=post_reactions)

@app.route('/view/<id>', methods = ['GET']) # Show specific post on whole page also displays any comments on the post
def view(id):
    form = CommentForm()
    post = Post.query.filter_by(id = id).first()
    comments = Comment.query.filter_by(post_id = id).all()
    comment_ids = [c.id for c in comments]
    reactions = Like.query.filter(Like.comment_id.in_(comment_ids)).all()  # Only reactions to comments

    # Build a dict: {comment_id: {'like_count': ..., 'dislike_count': ..., 'liked_by': [...], 'disliked_by': [...]}}
    comment_reactions = {}
    for comment in comments:
        likes = [r.username for r in reactions if r.comment_id == comment.id and r.is_like]
        dislikes = [r.username for r in reactions if r.comment_id == comment.id and not r.is_like]
        comment_reactions[comment.id] = {
            'like_count': len(likes),
            'dislike_count': len(dislikes),
            'liked_by': likes,
            'disliked_by': dislikes
        }

    return render_template('view.html.jinja', post = post, form = form, comments = comments, comment_reactions = comment_reactions)

@app.route('/images/<filename>') # Allows me to access images in folder instance (folder is created on run if it doesn't exist)
def get_image(filename):
    return send_from_directory(app.config['POST_UPLOAD_FOLDER'], filename)

@app.route('/view/post/<post_id>', methods = ['POST']) # Allows users to add comments to posts
@app.route('/view/post/<post_id>/<comment_id>', methods = ['POST']) # Allows users to add replies to existing comments
@login_required # Logged in users can add comments to posts
def add_comment(post_id, comment_id = None): 
    comment_time = int(time.time())
    form = CommentForm()
    comment = form.comment.data
    username = current_user.username
    print(comment_id)
    comment = Comment(
            post_id = post_id,
            username = username,
            content = comment,
            time = comment_time, # In db value stored is not date yet it gets converted to users local time with jinja when page is loaded
            parent_id = comment_id# If comment_id is provided it means that this comment is a reply to another comment else it is a top-level comment with parent_id set to None 
        )
    db.session.add(comment) # Adds comment to db
    db.session.commit()
    return redirect(f'/view/{post_id}') # Redirects to the post that was commented on

@app.route("/react/<int:post_id>", methods = ['POST']) # React to a post
@app.route("/react/<int:post_id>/<int:comment_id>", methods = ['POST']) # React to a comment 
@login_required # Login users can like/dislike
def like_dislike(post_id, comment_id = None):
    reaction = request.form.get('reaction') # Like or dislike string
    username = current_user.username
    if not comment_id: # If post will be liked
        react = Like.query.filter_by(post_id = post_id, username = username, comment_id = None).first() # Selects the post that will be reacted to
    else:
        react = Like.query.filter_by(post_id = post_id, username = username, comment_id = comment_id).first() # Selects the comment that will be reacted to
    
    if not react: # If user has not reacted to the post/comment yet
        react = Like(
            post_id = post_id,
            comment_id = comment_id,
            username = username,
            is_like = reaction == 'like' # True if like, False if dislike
        )
        db.session.add(react)
    else: # If user has already reacted to the post/comment
        react.is_like = reaction == 'like' # Updates the reaction to like or dislike

    db.session.commit() # Saves the change to db
    if not comment_id: # If post was liked/disliked
        return redirect('/posts') 
    else: # If comment was liked/disliked
        return redirect(f'/view/{post_id}')

@app.route('/home')
@login_required
def hello():
    return render_template('logged.html')

@app.route('/post', methods = ['GET', 'POST'])
@login_required
def post(): # Allow users to post messages for everyone
    form = PostForm()
    if request.method == 'POST':
        current_time = int(time.time()) # In seconds since epoch (Jan 1st 1970 UTC)
        username = current_user.username
        title = form.title.data
        post_content = form.post_content.data # Body of form
        post = Post(
            username = username,
            title = title,
            post_content = post_content,
            time = current_time # In db value stored is not date yet it gets converted to users local time with jinja when page is loaded
        )

        db.session.add(post)
        db.session.commit()

        files = form.images.data # Optional image of form
        if files: # If 0 logical statement results in false otherwise it is true
            jpg_images =  []
            for file in files:
                if allowed_file(secure_filename(file.filename)): # Checks if file has a valid suffix
                    img = Image.open(file) # Open img with Python image library
                    jpg_images.append(img.convert('RGB'))  # Convert opened image to jpg because it is much smaller
                else:
                    db.session.remove(post) # Removes previously uploaded post because user may have provided wrong input
                    db.session.commit()
                    return render_template("post.html", form = form, error='Only .jpg, .png, .jpeg, .gif and .webp are allowed. Post was not uploaded')
                
            post.image_count = len(jpg_images)
            for i, jpg_img in enumerate(jpg_images): # i will be a sign of how many images this post have 
                jpg_img.save(os.path.join(app.config['POST_UPLOAD_FOLDER'], str(i) + 'postimage_' + str(post.id) + '.jpg')) # Save it in a folder post_images in a folder instance

            db.session.commit()
        return redirect('/posts')

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
    if comment_id: # Comment will be deleted 
        comment = Comment.query.filter_by(id = comment_id).first()
        reactions = Like.query.filter_by(comment_id = comment_id).all()
        
        # Only if you are the commenter or the owner of the post
        if current_user.username == post.username or current_user.username == comment.username:
            for reaction in reactions: # Deletes all reactions to the comment
                db.session.delete(reaction)

            db.session.delete(comment)
            db.session.commit()

        return redirect(f'/view/{ post_id }')
    
    elif current_user.username == post.username: # Post will be deleted
        comments = Comment.query.filter_by(post_id = post_id).all()
        for comment in comments: # Deletes all comments on the post
            reactions = Like.query.filter_by(post_id = post_id, comment_id = comment.id).all()
            for reaction in reactions: # Deletes all reactions to the comment
                db.session.delete(reaction)
            db.session.delete(comment)

        reactions = Like.query.filter_by(post_id = post_id, comment_id = None).all()
        for reaction in reactions: # Deletes all reactions to the post itself
            db.session.delete(reaction)

        for i in range(post.image_count): # If post has images they will be deleted as well
            try:
                os.remove(os.path.join(app.config['POST_UPLOAD_FOLDER'], f'{i}postimage_' + str(post.id) + '.jpg')) # Deletes the image from the folder
            except Exception:
                pass

        db.session.delete(post)
        db.session.commit()
        return redirect('/posts')
    
    return redirect('/') # If you are not the owner of the post or comment you will be redirected to start page

