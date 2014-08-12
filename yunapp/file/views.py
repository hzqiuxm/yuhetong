# -*- coding: utf-8 -*-
import os, uuid
from flask import Blueprint, render_template, jsonify, request, config
import constants
mod_file = Blueprint('file', __name__)

@mod_file.route('/upload', methods=['POST'])
def upload():
    """ Upload file
    upload from user and store on server
    """
    file_upload = request.files['userfile']
    if file_upload and allowed_file(file_upload.filename):
        filename = generate_file_name()
        file_upload.save(os.path.join(constants.FILE_STORE_FOLDER, filename))
        return {"fid":"000","fname":'+filename+'}
    else:
        return {"fid":"000","errMsg":'error'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in constants.ALLOWED_EXTENSIONS

def generate_file_name():
    """ Generate file name use uuid
    May be replace with other generate method
    """
    return uuid.uuid1().hex