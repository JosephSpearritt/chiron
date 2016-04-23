"""

    Mange
    =====

    Management script for the Chiron application.

"""

import binascii
import os


from pathlib import Path

from chiron import app, db

from flask_script import Manager


manager = Manager(app)


def initialise_settings():
    """
    Function to create instance directory for the application.
    :return:
    """

    # Create directory if not exists.
    instance = Path(app.instance_path)
    if not instance.exists():
        instance.mkdir()

    # Create settings file.
    settings_file = instance / 'settings.py'
    if not settings_file.exists():
        with settings_file.open('w') as fh_out:
            fh_out.write('SECRET_KEY = "{}"\n'.format(binascii.hexlify(os.urandom(64)).decode()))

            fh_out.write('#TWILLIO_SID = "{}"\n')
            fh_out.write('#TWILLIO_TOKEN = "{}"\n')

            app.logger.warning('Created default config file, DO YOU NEED TWILIO CREDENTIALS?')

    # Load the configuration files
    app.config.from_pyfile('settings.py')


@manager.command
def run_debug():
    """
    Run the Chiron app in debug mode.
    """
    app.run(debug=True)

@manager.command
def initdb():
    """
    Setup the database
    """
    db.create_all()

if __name__ == '__main__':
    initialise_settings()
    manager.run()
