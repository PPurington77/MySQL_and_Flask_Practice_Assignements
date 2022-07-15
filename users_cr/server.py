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

@app.route('/update_user', methods=["POST"])
def update_user():

    User.update(request.form)

    return redirect('/')

@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/show_user/<int:id>')
def show(id):
    data = {
        "id":id
    }

    return render_template('show_user.html', user=User.get_one(data))

@app.route('/edit/<int:id>')
def edit(id):
    data = {
        "id":id
    }
    return render_template('edit.html', user=User.get_one(data))

@app.route('/destroy/<int:id>')
def destroy(id):
    data ={
        'id': id
    }
    User.destroy(data)
    return redirect('/')

if __name__=="__main__":
    app.run(debug=True)