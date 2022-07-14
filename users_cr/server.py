from flask import Flask, render_template, redirect, request
from users import User
app = Flask(__name__)

@app.route('/')
def read_all_users():
    all_users = User.get_all()
    print(all_users)
    return render_template('read.html', all_users = all_users)

@app.route('/create_user', methods=["POST"])
def create_user():
    data = {
        "first_name": request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email" : request.form['email']
        # "created_at" : request.form['created_at']
    }
    User.create(data)

    return redirect('/')

@app.route('/create')
def create():
    return render_template('create.html')

if __name__=="__main__":
    app.run(debug=True)