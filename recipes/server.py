from flask_app import app
#remember to add controller files as you build them
from flask_app.controllers import controller_users
from flask_app.controllers import controller_recipes


if __name__=="__main__":
    app.run(debug=True)
