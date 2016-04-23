"""

    Models
    ======

    Database backed models of useful classes.

"""


from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .app import db


class User(db.Model, UserMixin):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    passwordhash = db.Column(db.String)

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def __repr__(self):
        return '<User %s>' % self.username

    def set_password(self, password):
        self.passwordhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.passwordhash, password)

