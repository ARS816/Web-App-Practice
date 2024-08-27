from flask import render_template, request, redirect, flash, session
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe

@app.route('/recipes')
def all_recipes():
    data = {'id': session['id']}
    return render_template('dashboard.html', user = User.get_one(data), recipes = Recipe.get_all())

@app.route('/recipes/new')
def new_recipe():
    data = {'id': session['id']}
    return render_template('new_recipe.html', user = User.get_one(data))

@app.route('/recipes/new/add', methods=['POST'])
def add_recipe():
    if not Recipe.validate_recipe(request.form):
        return redirect ('/recipes/new')
    Recipe.save(request.form)
    return redirect('/recipes')
    
@app.route('/recipes/<int:id>')
def show_recipe(id):
    recipe = Recipe.get_by_id(id) 
    data = {'id': session['id']}
    user = User.get_one(data)
    return render_template('show_recipe.html', recipe = recipe, user = user)


@app.route('/recipes/edit/<int:id>')
def edit_recipe(id):
    recipe = Recipe.get_by_id(id)
    return render_template('edit_recipe.html', recipe = recipe)


@app.route('/recipes/edit/update', methods=['POST'])
def update_recipe():
    if not Recipe.validate_recipe(request.form):
        return redirect ('/recipes/new')
    Recipe.update(request.form)
    return redirect('/recipes')

@app.route('/recipes/delete/<int:id>')
def delete_post(id):
    Recipe.delete(id)
    return redirect('/recipes')