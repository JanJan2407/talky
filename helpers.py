'''Functions and classes that will be used in application'''

import datetime

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

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