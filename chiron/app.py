"""

    App.py
    ======

    Module to create the flask application instance.

"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager


app = Flask(__name__, instance_relative_config=True)
app.config.from_object(__name__)


# Load Extensions.
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

db = SQLAlchemy(app)