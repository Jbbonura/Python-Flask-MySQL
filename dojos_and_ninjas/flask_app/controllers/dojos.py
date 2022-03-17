from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.dojo import Dojo
from flask_app.models.ninja import Ninja

#@app.routes for dojos
@app.route('/')
@app.route('/dojos')
def dojos():
    dojos = Dojo.get_all()
    return render_template ('dojos.html', dojos = dojos)

@app.route('/dojos/<int:id>')
def showDojosNinjas(id):
    data = {
        'id' : id
    }
    dojo = Dojo.get_dojo_with_ninjas(data)
    return render_template('one_dojo.html', dojo = dojo)

@app.route('/create_dojo', methods =['POST'])
def create_dojo():
    data = {
        'name' : request.form['name']
    }
    Dojo.save_dojo(data)
    return redirect('/dojos')