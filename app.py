from hashlib import sha256
from flask import Flask
from flask import render_template
from flask import request

hash = hashlib.sha256()
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        answers = dict(request.form)
        if answers['pswrd'] == answers['pswrdcnfrm']: #password and pasword confirm
            hash_password = sha256(a['pswrd']) #hash password so it can be safely stored later
        else:
            pass #return passwords don't match
    return render_template('index.html')
  
