from flask_app import app, bcrypt
from flask import render_template, redirect, request, session, flash
from flask_app.models.model_user import User
from flask_app.models.model_recipe import Recipe


#Display
@app.route('/')
def home_page():
    if 'user' in session:
        user = session['user']
        return redirect(f'/welcome/{user}')
    return render_template('home.html')

#Action
@app.route('/register', methods=["POST"])
def register():
    is_valid = User.validate(request.form)
    if not is_valid:
        print(is_valid)
        return redirect('/')

    hash_pw = bcrypt.generate_password_hash(request.form['password'])

    data = {
        **request.form, 
        'password' : hash_pw
    }

    user = User.create(data)
    session['user'] = user
    print(user)

    return redirect(f'/welcome/{user}')

#Display
@app.route('/welcome/<int:id>')
def welcome(id):
    data = {
        'id' : id 
    }

    if 'user' not in session:
        return redirect ('/')

    return render_template('welcome.html', user = User.get_one(data), all_recipes = Recipe.get_all())

@app.route('/login', methods=["POST"])
def login():
    
    is_valid = User.validate_login(request.form)

    if not is_valid:
        print('not correct')
        return redirect('/')

    data = {
        **request.form
    }

    user_id = User.get_one_login(data)
    user = user_id.id
    session['user'] = user

    return redirect (f'/welcome/{user}')

# #Action
@app.route('/logout', methods=['GET'])
def logout():

    session.clear()

    return redirect('/')