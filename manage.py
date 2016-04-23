"""

    Mange
    =====

    Management script for the Chiron application.

"""

from chiron.models import User
from flask_script import Manager

from chiron import app, db

manager = Manager(app)


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


@manager.command
def make_dummy_users():
    """
    Set the db up with dummy user stuff
    """
    dummyuser = User('Bob', 'iamanurse')
    db.session.add(dummyuser)
    db.session.commit()


if __name__ == '__main__':
    manager.run()
