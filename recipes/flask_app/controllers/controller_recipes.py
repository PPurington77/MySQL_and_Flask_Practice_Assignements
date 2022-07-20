from flask_app import app, bcrypt
from flask import render_template, redirect, request, session, flash
from flask_app.models.model_user import User
from flask_app.models.model_recipe import Recipe
from flask_app.models import model_recipe #to use context


@app.route('/add_recipe')
def add_recipe():

    return render_template('add_recipe.html', user = session['user'])

#Action 
@app.route('/create_recipe', methods=['POST'])
def create_recipe():
    is_valid = Recipe.validate(request.form)
    if not is_valid:
        print(is_valid, 'not validating recipe')
        return redirect('/add_recipe')

    data = {
        **request.form,
        'user_id' : session['user']
    }
    user = session['user']
    recipe = Recipe.create(data)
    print(recipe, 'created')

    return redirect(f'/welcome/{user}')

@app.route('/welcome/view/recipe/<int:id>')
def view_recipe(id):
    data = {
        'id':id
    }
    
    #question regarding pushing user info to sheet
    return render_template('view_recipe.html', recipe = Recipe.get_one_user_from_recipes(data), user = session['user'])

@app.route('/edit/<int:id>/edit')
def edit_recipe_view(id):
    context = {
        'recipe' : model_recipe.Recipe.get_one({'id':id})
    }
    return render_template('edit_recipe.html', **context)

@app.route('/edit/<int:id>/update', methods=['POST'])
def edit_recipe(id):
    if not model_recipe.Recipe.validate(request.form):
        return redirect (f'/edit/{id}/edit')

    data = {
        **request.form, 
        'id':id
    }
    user = session['user']
    model_recipe.Recipe.update(data)

    return redirect(f'/welcome/{user}')

@app.route('/delete/<int:id>')
def delete(id):
    data ={
        'id': id
    }
    # if recipe.user_id != session['id']: a way to further secure for future ref
    #     flash('you cant do that')
    Recipe.delete(data)
    return redirect('/')