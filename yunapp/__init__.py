# -*- coding: utf-8 -*-
# @author: wenwu

import jinja2, sys

from flask import render_template
# from flask.ext.admin import Admin
from flask_wtf.csrf import CsrfProtect

from test.views import test as mod_test
from user.views import user as mod_user
from file.views import mod_file
from contract.view import contract as mod_contract
from contract_temp.views import template as mod_c_template
from yunapps import app
from yunapp import utils, logutils

from yunapp.web.users import web_users
from yunapp.web.ctemplates import web_templates
# Admin import may be delete online
# from yunapp.admin.contract_template_admin import ComtractTemplateAdminView
# from flask.ext.admin.contrib.sqla import ModelView
from yunapp.orm import model, engine

logutils.init_log()

my_loader = jinja2.ChoiceLoader([
    app.jinja_loader,
    jinja2.FileSystemLoader( app.root_path +
    '/templates'),
])
app.jinja_loader = my_loader

# Blueprint Register
app.config.from_object('config')
app.register_blueprint(mod_test, url_prefix='/api/test')
app.register_blueprint(mod_user, url_prefix='/api/user')
app.register_blueprint(mod_file, url_prefix='/api/file')
app.register_blueprint(mod_c_template, url_prefix='/api/ctemplate')
app.register_blueprint(mod_contract, url_prefix='/api/contract')

# Flask-admin should be delete
# admin = Admin(app, name='Yunhetong')
# admin.add_view(ComtractTemplateAdminView(name='Contract Template'))
# admin.add_view(ModelView(model.LxTempTyp  e, engine.s))

# Blueprint Register for web
app.register_blueprint(web_users, url_prefix='/user')
app.register_blueprint(web_templates, url_prefix='/ctemplate')

CsrfProtect(app)

@app.route("/sitemap.html", methods=['GET'])
def site_map():
    return utils.show_site_map(app.url_map.iter_rules())

@app.route("/index", methods=['GET'])
def yunapp_index():
    return render_template('newhome.html')
