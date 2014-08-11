# -*- coding: utf-8 -*-
# @author: wenwu

from flask import Flask
from test.views import test as mod_test
from user.views import user as mod_user
app = Flask('yunhetong')

app.register_blueprint(mod_test, url_prefix='/test')
app.register_blueprint(mod_user, url_prefix='/user')


