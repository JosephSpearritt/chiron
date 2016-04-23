from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

# Configuration
SECRET_KEY = 'adatabasekey'
SQLALCHEMY_DATABASE_URI = 'sqlite:///chiron.db'

app = Flask(__name__)
app.config.from_object(__name__)

login_manager = LoginManager()
login_manager.login_view = 'login';
login_manager.init_app(app)

db = SQLAlchemy(app)