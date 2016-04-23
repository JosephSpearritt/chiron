"""
    Chiron.views
    ============

    URL routes for the project.

"""

from datetime import datetime

from flask import (render_template,
                   request, redirect,
                   url_for,
                   flash,
                   jsonify,
                   abort,
                   )
from flask.ext.login import login_required, login_user, logout_user, current_user

from . import app
from .app import login_manager
from .models import *
from .tanda import *

@app.route('/')
def index():
    """
    Base route for the website.
    """
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    reqs = LeaveRequest.query.filter_by(status=0).all()
    return render_template('dashboard.html', reqs=reqs)


@app.route('/receivesms', methods=['POST'])
def receive_sms():
    """
    Endpoint for twillio to send received texts to.
    :return:
    """
    app.logger.info(request.values)
    with open('texts.txt', 'a') as fh:
        fh.write('{}: {}\n\n'.format(datetime.now().isoformat(), str(dict(request.values.items()))))

    # Populate a dictionary with sms data.
    keys = ['Body', 'From']
    sms_dictionary = {}
    for key in keys:
        if not request.values.get(key):
            return abort(400)
        sms_dictionary[key.lower()] = request.values[key]

    # SAM: SMS keys are 'from', 'body', and are both strings
    receive_text(sms_dictionary['from'],sms_dictionary['body'])
    return jsonify(sms_dictionary)


@app.route('/approve/<reqid>', methods=['GET'])
@login_required
def approve_request(reqid):
    req = LeaveRequest.query.filter_by(id=reqid).first()
    if req is None:
        flash('Request not found')
        return redirect(url_for('dashboard'))
    req.status = 1
    db.session.commit()

    # DO TANDA STUFF

    return redirect(url_for('dashboard'))


@app.route('/deny/<reqid>', methods=['GET'])
@login_required
def deny_request(reqid):
    req = LeaveRequest.query.filter_by(id=reqid).first()
    if req is None:
        flash('Request not found')
        return redirect(url_for('dashboard'))
    req.status = -1
    db.session.commit()
    return redirect(url_for('dashboard'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        sqlUser = User.query.filter_by(username=request.form.get('username', ''))
        if sqlUser.count() == 1:
            if sqlUser.first().check_password(request.form.get('password', '')):
                login_user(sqlUser.first())
                flash('Successfully logged in as %s' % request.form.get('username', ''))
                try:
                    next = request.form['next']
                    return redirect(next)
                except:
                    return redirect(url_for('index'))
            else:
                flash('Login failed!')
                return redirect(url_for('login'))
        else:
            flash('Login failed!')
            return redirect(url_for('login'))
        return

    # Render the login page
    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    flash('Logged out!')
    return redirect(url_for('index'))


@login_manager.user_loader
def user_loader(user_id):
    user = User.query.filter_by(id=user_id)
    if user.count() == 1:
        return user.one()
    return None
