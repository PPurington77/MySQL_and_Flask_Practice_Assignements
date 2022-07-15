from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.ninja import Ninja
from flask_app.models.dojo import Dojo

@app.route('/ninjas')
def ninjas():
    all_ninjas = Ninja.get_all()
    all_dojos = Dojo.get_all()
    print(all_ninjas)
    return render_template('new_ninja.html', all_ninjas = all_ninjas, all_dojos = all_dojos)

#Action
@app.route('/create_ninja', methods=["POST"])
def create_ninja():
    Ninja.create(request.form)

    return redirect ('/dojos')