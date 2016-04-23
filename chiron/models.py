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


class LeaveRequest(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer)
    employee_phone = db.Column(db.String)
    date = db.Column(db.Date)
    leave_reason = db.Column(db.String)
    status = db.Column(db.Integer)

    def __init__(self, employee_id, employee_phone="None", leave_reason="No Reason", date=None, status=0):
        self.employee_id = employee_id
        self.employee_phone = employee_phone
        self.leave_reason = leave_reason
        self.date = date
        self.status = status
