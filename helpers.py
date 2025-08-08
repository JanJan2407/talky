'''Functions and classes that will be used in application'''

import datetime
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