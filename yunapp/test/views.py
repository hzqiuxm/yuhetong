# -*- coding: utf-8 -*-

from flask import Blueprint, render_template
test = Blueprint('test', __name__)

@test.route('/')
def hello_world():
    return 'Hello World!'


@test.route('/<path:filename>')
def template_load(filename=None):
    if not filename:
        return render_template('index.html')
    else:
        return render_template(filename+'.html')