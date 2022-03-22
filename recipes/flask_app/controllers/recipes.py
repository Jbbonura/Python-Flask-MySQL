from flask_app import app
from flask import render_template, request, redirect, session, flash

from flask_app.models.recipe import Recipe

##!CREATE
## TODO Show the new recipe form
@app.route('/recipes/new')
def new_recipe():
    return render_template('new_recipe.html')

## TODO handle new recipe form
@app.route('/create/recipe', methods=['POST'])
def create_recipe():
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes/new')
    recipe = Recipe.save(request.form) #! class method in recipe class, find it in ../controllers/recipe.py
    
    return redirect(f"/recipes/{recipe}")


##! READ
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash("please log in or register")
        return redirect('/')
    return render_template('recipes.html', recipes = Recipe.get_all())

@app.route('/recipes/<int:id>')
def show_recipe(id):
    data = {'id': id}
    return render_template('show_recipe.html', recipe = Recipe.get_one(data))


#! UPDATE
## TODO route to edit recipe form
@app.route('/recipes/edit/<int:id>')
def edit_recipe(id):
    data = {'id': id}
    recipe = Recipe.get_one(data)
    return render_template('edit_recipe.html', recipe = recipe)

## TODO handle recipe edit
@app.route('/edit/recipe', methods=['POST'])
def update_recipe():
    print(request.form)
    recipe = Recipe.update(request.form)
    print(recipe)
    return redirect("/dashboard")

@app.route('/delete/<int:id>')
def delete_recipe(id):
    data = {
        'id' : id
    }
    Recipe.destroy(data)
    return redirect('/dashboard')
