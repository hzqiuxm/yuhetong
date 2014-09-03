# -*- coding:utf-8 -*-
import requests
from flask.ext.script import Manager
from yunapp.yunapps import app
from yunapp.orm.model import db

manager = Manager(app)

@manager.command
def createdb():
    db.create_all()

@manager.command
def init_temptype():
    r = requests.get('http://yunhetong.com:8091/api/ctemplate/init_template_type')
    print r.status_code

if __name__ == "__main__":
    manager.run()
