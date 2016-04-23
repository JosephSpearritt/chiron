from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Configuration
SECRET_KEY = 'adatabasekey'
SQLALCHEMY_DATABASE_URI = 'sqlite:///chiron.db'

app = Flask(__name__)
app.config.from_object(__name__)

db = SQLAlchemy(app)