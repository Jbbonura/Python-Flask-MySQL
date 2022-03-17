from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
@app.route('/users')
def index():
    users = User.get_all()
    return render_template('index.html', users = users)

@app.route('/users/new')
def newUser():
    return render_template('create.html')

@app.route('/create', methods =['POST'])
def create():
    data = {
        'fname': request.form['fname'],
        'lname': request.form['lname'],
        'email': request.form['email']
    }
    User.save(data)
    return redirect('/users')

@app.route('/users/<int:id>')
def read(id):
    data = {
        'id' : id
    }
    user = User.get_one(data)
    return render_template('read.html', user = user)

@app.route('/users/<int:id>/edit')
def edit(id):
    data = {
        'id': id
    }
    user = User.get_one(data)
    return render_template('edit.html', user = user)

@app.route('/update', methods=['POST'])
def update():
    print(request.form)
    data = {
        'id' : request.form['id'],
        'fname': request.form['fname'],
        'lname': request.form['lname'],
        'email': request.form['email']
    }
    User.update_one(data)
    return redirect ('/users')

@app.route('/delete/<int:id>')
def delete(id):
    data = {
        'id' : id
    }
    User.delete_one(data)
    return redirect('/users')