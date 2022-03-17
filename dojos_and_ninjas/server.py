from flask_app import app
from flask_app.controllers import dojos # <-- change to name of file in controllers
from flask_app.controllers import ninjas # <-- change to name of file in controllers

if __name__ == "__main__":
    app.run(debug = True)