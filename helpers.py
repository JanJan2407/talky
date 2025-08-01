'''Functions and classes that will be used in application'''

def valid_error(error):
    allowed_errors = ['Please log in to access that'] # In future I'll add more
    return error in allowed_errors