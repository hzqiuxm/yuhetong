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

    test_user = {'username': 'lxTest@yunhetong.com', 'password': 'lxTest', 'email': 'lxTest@yunhetong.com',
                 'type': '0','real_name': 'seanwu', 'phone': '123456789'}
    r = requests.post('http://' + config.SERVER_NAME + '/api/user/register',
                      data=test_user)

    print r.status_code


if __name__ == "__main__":
    manager.run()
