# -*- coding: utf-8 -*-

from flask import Blueprint, render_template

import os
from flask import Flask, request, redirect, url_for
#from werkzeug import secure_filename

# UPLOAD_FOLDER = '/home/seanwu/uploads/'
# ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
#
# test.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

test = Blueprint('test', __name__)


@test.route('/')
def hello_world():
    return render_template('index.html')

@test.route('/file/upload', methods=['GET', 'POST'])
def file_upload():
    return '{"fid":"000"}'

@test.route('/<path:filename>')
def template_load(filename=None):
    if not filename:
        return render_template('index.html')
    else:
        return render_template(filename+'.html')

