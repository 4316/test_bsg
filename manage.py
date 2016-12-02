from flask_script import Manager, Server, Shell
from source_code import application
from source_code.commands import ManagerInstead

manager = Manager(application)


def _make_context():
    """Return context dict for a shell session so you can access
    app, db, and the User model by default.
    """
    return {'application': application}


@manager.command
def init_db():
    ManagerInstead.initdb()


manager.add_command("runserver", Server(use_debugger=True, use_reloader=True, host='127.0.0.1'))
manager.add_command('shell', Shell(make_context=_make_context))

if __name__ == '__main__':
    manager.run()
