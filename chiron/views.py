"""
    Chiron.views
    ============

    URL routes for the project.

"""

from flask import render_template, request, redirect, url_for, flash
from flask.ext.login import login_required, login_user, logout_user, current_user

from . import app
from .app import login_manager
from .models import *


@app.route('/')
def index():
    """
    Base route for the website.
    """
    return render_template('dashboard.html')


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
    return redirect(url_for('index'))