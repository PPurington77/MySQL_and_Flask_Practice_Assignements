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

    User.create(request.form)

    return redirect('/')

@app.route('/create')
def create():
    return render_template('create.html')

if __name__=="__main__":
    app.run(debug=True)