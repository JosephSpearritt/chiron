"""

    Mange
    =====

    Management script for the Chiron application.

"""


from chiron import app, db

from flask_script import Manager


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

if __name__ == '__main__':
    manager.run()