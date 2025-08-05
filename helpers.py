'''Functions and classes that will be used in application'''

import datetime

def valid_error(error):
    allowed_errors = ['Please log in to access that'] # In future I'll add more
    return error in allowed_errors
    
def get_date(epoch): # Returns datetime object used with flask moment to display date 
    date = datetime.datetime.fromtimestamp(epoch , datetime.UTC)
    return date
