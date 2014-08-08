# -*- coding: utf-8 -*-
# @author: wenwu

from flask import Flask
from test.views import test as mod_test
app = Flask('yunhetong')

app.register_blueprint(mod_test,url_prefix='/test')

