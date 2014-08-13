# -*- coding: utf-8 -*-
# @author: wenwu


from test.views import test as mod_test
from user.views import user as mod_user
from file.views import mod_file
from yunapps import app
import jinja2
my_loader = jinja2.ChoiceLoader([
    app.jinja_loader,
    jinja2.FileSystemLoader( app.root_path +
    '/yunapp/templates'),
])
app.jinja_loader = my_loader

app.config.from_object('config')

app.register_blueprint(mod_test, url_prefix='/test')
app.register_blueprint(mod_user, url_prefix='/user')
app.register_blueprint(mod_file, url_prefix='/file')


