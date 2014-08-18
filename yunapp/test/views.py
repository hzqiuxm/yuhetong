# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, send_file, jsonify
import os
from flask import Flask, request, redirect, url_for
from yunapp.yunapps import app

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

test = Blueprint('test', __name__)

UPLOAD_FOLDER = '/home/seanwu/uploads/'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@test.route('/')
def hello_world():
    return render_template('index.html')


@test.route('/file/upload', methods=['POST'])
def file_upload():
    if request.method == 'POST':
        file = request.files['userfile']
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return {"fid": "000", "fname": '+filename+'}
        else:
            return {"fid": "000", "errMsg": 'error'}

@test.route('/<path:filename>')
def template_load(filename=None):
    if not filename:
        return render_template('index.html')
    else:
        return render_template('/test/' + filename)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
