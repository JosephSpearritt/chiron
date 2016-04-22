"""

    Mange
    =====

    Management script for the Chiron application.

"""


from chiron import app

from flask_script import Manager


manager = Manager(app)


@manager.command
def run_debug():
    """
    Run the Chiron app in debug mode.
    """
    app.run(debug=True)


if __name__ == '__main__':
    manager.run()
