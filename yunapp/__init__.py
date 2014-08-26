# -*- coding: utf-8 -*-
# @author: wenwu

from test.views import test as mod_test
from user.views import user as mod_user
from file.views import mod_file
from contract.view import contract as mod_contract
from contract_temp.views import template as mod_c_template
from yunapps import app
from yunapp import utils, logutils
import jinja2
from flask import render_template

logutils.init_log()

my_loader = jinja2.ChoiceLoader([
    app.jinja_loader,
    jinja2.FileSystemLoader( app.root_path +
    '/templates'),
])
app.jinja_loader = my_loader

app.config.from_object('config')
app.register_blueprint(mod_test, url_prefix='/test')
app.register_blueprint(mod_user, url_prefix='/user')
app.register_blueprint(mod_file, url_prefix='/file')
app.register_blueprint(mod_c_template, url_prefix='/ctemplate')
app.register_blueprint(mod_contract, url_prefix='/contract')

@app.route("/sitemap.html", methods=['GET'])
def site_map():
    return utils.show_site_map(app.url_map.iter_rules())

@app.route("/index.html", methods=['GET'])
def index():
    return render_template("/index.html")
