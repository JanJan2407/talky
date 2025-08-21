'''Functions and classes that will be used in application'''

import datetime
import os
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'gif'} # Allowed image extensions

def valid_error(error):
    allowed_errors = ['Please log in to access that'] # In future I'll add more
    return error in allowed_errors
    
def get_date(epoch): # Returns datetime object used with flask moment to display date 
    date = datetime.datetime.fromtimestamp(epoch , datetime.UTC)
    return date

def allowed_file(filename): # Checks if file is allowed (has an allowed suffix (extension))
    try:
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    except Exception: # If file doesn't have a suffix at all
        return False
    
def get_replies(parent_id): # Get all replies to a specific comment via parent comment id
    from models import Comment # Import down here because we don't want circular import error 
    return Comment.query.filter_by(parent_id = parent_id).all()
    
def get_reactions(post_id = None, comment_id = None):
    ''' Get all reactions from a specific post/comment '''
    from models import Like # Import here to avoid import loop

    if post_id:
        reactions = Like.query.filter_by(post_id = post_id).all()  # Get all reactions for a specific post
    elif comment_id:
        reactions = Like.query.filter_by(comment_id = comment_id).all()  # Get all reactions for a specific comment
    else:
        return {} # If nothing is provided
    likes = [r.username for r in reactions if r.is_like] # Get usernames of users who liked the post/comment
    dislikes = [r.username for r in reactions if not r.is_like] # Get usernames of users who disliked the post/comment
    reactions_dict = {
        'like_count': len(likes),
        'dislike_count': len(dislikes),
        'liked_by': likes,
        'disliked_by': dislikes
    }
    return reactions_dict

def validate(post_id, image_count):
    ''' Get all valid images unter a specific post '''
    from resources import app

    valid_images = []
    for i in range(image_count):
        f_path = os.path.join(app.config['POST_UPLOAD_FOLDER'], f'{post_id}postimage_{i}.jpg')
        if os.path.exists(f_path):
            valid_images.append(i)

    return valid_images
