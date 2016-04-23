"""

    App.py
    ======

    Module to create the flask application instance.

"""
import binascii
import os
from pathlib import Path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager


def initialise_settings(application):
    """
    Function to create instance directory for the application.
    :return:
    """

    # Create directory if not exists.
    instance = Path(application.instance_path)
    if not instance.exists():
        instance.mkdir()

    # Create settings file.
    settings_file = instance / 'settings.py'
    if not settings_file.exists():
        with settings_file.open('w') as fh_out:
            fh_out.write('SECRET_KEY = "{}"\n'.format(binascii.hexlify(os.urandom(64)).decode()))
            fh_out.write('SQLALCHEMY_DATABASE_URI = "sqlite:///chiron.db"\n')
            fh_out.write('SQLALCHEMY_TRACK_MODIFICATIONS = False\n')

            fh_out.write('#TWILLIO_SID = "{}"\n')
            fh_out.write('#TWILLIO_TOKEN = "{}"\n')

            fh_out.write('TANDA_TOKEN = #"Tanda OAuth token here!"\n')

            application.logger.warning('Created default config file, DO YOU NEED TWILIO CREDENTIALS?')

    # Load the configuration files
    application.config.from_pyfile('settings.py')


def create_app():
    """
    Factory function for flask application.
    :return:
    """

    app = Flask(__name__, instance_relative_config=True)

    initialise_settings(app)

    return app


app = create_app()


# Load Extensions.
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

db = SQLAlchemy(app)