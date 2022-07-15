from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.dojo import Dojo
from flask_app.models.ninja import Ninja

#Display
@app.route('/dojos')
def dojos():
    all_dojos = Dojo.get_all()
    print(all_dojos)
    return render_template('dojos.html', all_dojos = all_dojos)

#Action
@app.route('/create_dojo', methods=["POST"])
def create_dojo():
    Dojo.create(request.form)

    return redirect ('/dojos')

#Display
@app.route('/show_dojo/<int:id>')
def show_dojo(id):
    data = {
        'id':id 
    }
    return render_template('show_dojo.html', dojo = Dojo.get_one(data))