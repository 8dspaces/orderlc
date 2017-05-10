# -*- coding: utf-8 -*-
"""Create an application instance."""
from flask.helpers import get_debug_flag
from orderlc.user.models import User
from orderlc.app import create_app
from orderlc.settings import DevConfig, ProdConfig

# from orderlc.public.models import Script, Job, STATUS_WAITING, STATUS_COMPLETE, STATUS_ERROR, STATUS_RUNNING
from flask_script import Manager

from flask_script import Manager, Shell, Server
from flask_migrate import MigrateCommand
from orderlc.database import db


from orderlc.public.models import Customer, Good, Container

# import logging
# logging.basicConfig(level=logging.DEBUG)

CONFIG = DevConfig if get_debug_flag() else DevConfig #ProdConfig

app = create_app(CONFIG)

manager = Manager(app)

def _make_context():
    """Return context dict for a shell session so you can access
    app, db, and the User model by default.
    """
    return {'app': app, 'db': db, 'User': User,'Customer':Customer,'Good':Good,'Container':Container}


@manager.command
def test():
    """Run the tests."""
    import pytest
    exit_code = pytest.main([TEST_PATH, '--verbose'])
    return exit_code

manager.add_command('server', Server())
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
