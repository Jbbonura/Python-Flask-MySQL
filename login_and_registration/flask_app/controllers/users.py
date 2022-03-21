from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User #<--models.(fileName) import (className)


#place all @app.routes here change file name to plural of class

@app.route('/')
def index():

    return render_template('index.html')


@app.route('/create_user', methods=['POST'])
def register():
    if not User.validate_form(request.form):
        # we redirect to the template with the form.
        return redirect('/')
    
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    # put the pw_hash into the data dictionary
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password" : pw_hash
    }
    # Call the save @classmethod on User
    user_id = User.save(data)
    # store user id into session
    session['user_id'] = user_id
    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    # see if the username provided exists in the database
    data = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(data)
    # user is not registered in the db
    print(user_in_db.password)
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # if we get False after checking the password
        flash("Invalid Email/Password")
        return redirect('/')
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id
    # never render on a post!!!
    return redirect("/dashboard")

@app.route('/dashboard')
def dashboard():
    data = {
        'id' : session['user_id']
    }
    
    return render_template('dashboard.html', user = User.get_one_by_id(data))

@app.route('/logout', methods=['Post'])
def logout():
    session.clear()
    return redirect('/')
