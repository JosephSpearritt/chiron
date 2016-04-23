"""
    Chiron.views
    ============

    URL routes for the project.

"""

from flask import render_template

from . import app
from .models import *


@app.route('/')
def index():
    """
    Base route for the website.
    """
    return render_template('dashboard.html')
