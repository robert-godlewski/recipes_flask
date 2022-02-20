from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask import render_template, redirect, session, request


@app.route('/recipes/new')
def new_recipe():
    if 'user_id' not in session:
        return redirect('/logout')
    user_data = {
        "id": session['user_id']
    }
    return render_template("new_recipe.html", user=User.get_one(user_data))

@app.route('/recipe/create', methods=['POST'])
def create_recipe():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes/new')
    data = {
        "name": request.form['name'],
        "description": request.form['description'],
        "instructions": request.form['instructions'],
        "date_made": request.form['date_made'],
        "under_30_min": int(request.form['under_30_min']),
        "user_id": session['user_id']
    }
    Recipe.save_recipe(data)
    return redirect('/dashboard')

@app.route('/recipes/<int:id>')
def show_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    user_data = {
        "id": session['user_id']
    }
    recipe_info = Recipe.get_recipe(data)
    user_info = User.get_one(user_data)
    return render_template("show_recipe.html", user=user_info, recipe=recipe_info)

@app.route('/recipes/edit/<int:id>')
def edit_recipe(id): 
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    user_data = {
        "id": session['user_id']
    }
    recipe_info = Recipe.get_recipe(data)
    user_info = User.get_one(user_data)
    # might need to fix the HTML link
    return render_template("edit_recipe.html", user=user_info, recipe=recipe_info)

# Might need to fix later on
@app.route('/recipes/update', methods=['POST'])
def update_recipe():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Recipe.validate_recipe(request.form):
        return redirect('/dashboard')
    data = {
        "id": request.form['id'],
        "name": request.form['name'],
        "description": request.form['description'],
        "instructions": request.form['instructions'],
        "date_made": request.form['date_made'],
        "under_30_min": int(request.form['under_30_min'])
    }
    Recipe.edit_recipe(data)
    return redirect('/dashboard')

@app.route('/recipes/destroy/<int:id>')
def destroy_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    Recipe.destroy_recipe(data)
    return redirect('/dashboard')
