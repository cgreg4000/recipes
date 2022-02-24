from crypt import methods
import re
from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user_model import User
from flask_app.models.recipe_model import Recipe

@app.route('/dashboard')
def welcome():

    if not session:
        flash("Please login to access this site.")
        return redirect('/')

    recipes = Recipe.get_all_recipes()

    return render_template('dashboard.html', recipes = recipes)

@app.route('/recipes/new')
def new_recipe():

    if not session:
        flash("Please login to access this site.")
        return redirect('/')

    return render_template('new_recipe.html')

@app.route('/recipes/create', methods=['POST'])
def create_recipe():

    if not Recipe.validate_recipe(request.form):
        print("NOT VALID")
        return redirect('/recipes/new')

    data = {
        'recipe_name' : request.form['recipe_name'],
        'recipe_description' : request.form['recipe_description'],
        'recipe_instructions' : request.form['recipe_instructions'],
        'recipe_date' : request.form['recipe_date'],
        'under_30' : request.form['under_30'],
        'user_id' : session['user_id']
    }

    Recipe.create_recipe(data)

    return redirect('/dashboard')

@app.route('/recipes/<int:recipe_id>')
def recipe_details(recipe_id):

    data = {
        'id' : recipe_id
    }

    recipe = Recipe.get_recipe_by_id(data)

    return render_template('recipe_details.html', recipe = recipe)

@app.route('/recipes/edit/<int:recipe_id>')
def edit_recipe(recipe_id):

    if not session:
        flash("Please login to access this site.")
        return redirect('/')

    data = {
        'id' : recipe_id
    }

    recipe = Recipe.get_recipe_by_id(data)

    return render_template('edit_recipe.html', recipe = recipe)

@app.route('/recipes/<int:recipe_id>/update', methods=['POST'])
def update_recipe(recipe_id):

    if not Recipe.validate_recipe(request.form):
        print("NOT VALID")
        return redirect(f'/recipes/edit/{recipe_id}')
    
    
    data = {
        'recipe_id' : recipe_id,
        'recipe_name' : request.form['recipe_name'],
        'recipe_description' : request.form['recipe_description'],
        'recipe_instructions' : request.form['recipe_instructions'],
        'recipe_date' : request.form['recipe_date'],
        'under_30' : request.form['under_30']
    }
    
    Recipe.update_recipe(data)

    return redirect('/dashboard')

@app.route('/recipes/<int:recipe_id>/delete')
def delete_recipe(recipe_id):

    data = {
        'id' : recipe_id
    }

    Recipe.delete_recipe(data)

    return redirect('/dashboard')