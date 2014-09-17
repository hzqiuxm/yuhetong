# -*- coding:utf-8 -*-
import requests
from flask.ext.script import Manager
from yunapp.yunapps import app
from yunapp.orm.model import db
from yunapp import config

manager = Manager(app)


@manager.command
def createdb():
    db.create_all()


@manager.command
def init_temptype():
    r = requests.get('http://' + config.SERVER_NAME +
                     '/api/ctemplate/init_template_type')
    print r.status_code


@manager.command
def init_user():
    r = requests.get('http://' + config.SERVER_NAME +
                     '/api/user/init_test_user')

    print r.status_code


if __name__ == "__main__":
    manager.run()
