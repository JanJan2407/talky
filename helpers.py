'''Functions and classes that will be used in application'''
import time
import datetime

def valid_error(error):
    allowed_errors = ['Please log in to access that'] # In future I'll add more
    return error in allowed_errors
    

class PostTime:
    # Input is an integer-time since epoch from time module 
    def __init__(self, input): 
        self.time = input 

    def display_time(self): # Returns a list with time zone adjusted for user viewing it
        output = []
        time_struct = time.localtime(self.time)
        for i in range(6): # Appends first 6 values in users localtime being 
            output.append(time_struct[i])


def get_date(epoch): # Returns datetime object used with flask moment to display date 
    date = datetime.datetime.fromtimestamp(epoch , datetime.UTC)
    return date
