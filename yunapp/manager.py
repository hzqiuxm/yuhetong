# -*- coding:utf-8 -*-

from flask.ext.script import Manager
from yunapp.yunapps import app
from yunapp.orm.model import db

manager = Manager(app)

@manager.command
def createdb():

    db.create_all()


if __name__ == "__main__":
    manager.run()