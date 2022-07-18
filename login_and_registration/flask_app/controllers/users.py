from flask_app import app, bcrypt
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User

#Dispaly
@app.route('/')
def home_page():

    return render_template('index.html')

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

    user_id = User.create(data)
    session['user_id'] = user_id
    print(user_id)
    return redirect(f'/welcome/{user_id}')

#Display
@app.route('/welcome/<int:id>')
def welcome(id):
    data = {
        'id' : id 
    }
    return render_template('welcome.html', user = User.get_one(data))

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
    login_id = user_id.id
    print(login_id)

    # session['user_email'] = user_email
    # print(user_email)
    return redirect (f'/welcome/{login_id}') # in selecting I'm not getting an id return...need to figure out

#Display
# @app.route('/welcome_user/<email>')
# def welcome_user(email):
#     data = {
#         'email':email
#     }
#     return render_template('welcome.html', user = User.get_one(data))

#Action
@app.route('/logout', methods=['GET'])
def logout():
    # if session == True:
    #     print('in session')
    # else:
    #     print('not in session')
    # session.clear()
    ##FOR SOME REASON SESSION IS NOT WORKING...CAN'T FIGURE IT OUT FOR NOW...
    return redirect('/')