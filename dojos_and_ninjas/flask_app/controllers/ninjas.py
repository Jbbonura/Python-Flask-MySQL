from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.ninja import Ninja
from flask_app.models.dojo import Dojo

#@app.routes for ninja
@app.route('/ninjas')
def ninjas():
    dojos = Dojo.get_all()
    return render_template('ninjas.html', dojos = dojos)

@app.route('/create_ninja', methods=['POST'])
def create_ninja():
    dataName = {
        'name' : request.form['dojos']
    }
    dojo = Dojo.get_one_by_name(dataName)
    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'age' : request.form['age'],
        'dojo_id' : dojo.id
    }
    Ninja.save_ninja(data)
    return redirect(f"/dojos/{data['dojo_id']}")