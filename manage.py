#! env/bin/python
# -*- coding:utf-8 -*-

import os  # set root path
import sys
PROJECT_ROOT = os.path.join(os.path.realpath(os.path.dirname(__file__))).replace('\\', '/')
sys.path.append(os.path.join(PROJECT_ROOT, 'spellworks'))

from spellworks import create_app, db
from flask.ext.script import Manager, Shell, Server


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)


def make_shell_context():
    return dict(app=app, db=db)
manager.add_command("shell", Shell(make_context=make_shell_context))


server = Server(host="0.0.0.0", port=5000, use_reloader=True)
manager.add_command("runserver", server)


if __name__ == '__main__':
    manager.run()
