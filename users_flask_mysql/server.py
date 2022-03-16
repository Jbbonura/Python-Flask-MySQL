from flask import Flask, render_template, redirect, request
from user import User

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(debug = True)