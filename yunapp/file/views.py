# -*- coding: utf-8 -*-
import os, uuid
from flask import Blueprint, render_template, jsonify, request, config
import constants
from yunapp.orm.model import LxFile
mod_file = Blueprint('file', __name__)

@mod_file.route('/upload', methods=['POST'])
def upload():
    """ Upload file
    upload from user and store on server
    """
    file_upload = request.files['userfile']
    if file_upload and allowed_file(file_upload.filename):
        if is_static_file(file_upload.filename):
            file_type = 1
        else:
            file_type = 2
        fuuid = generate_file_uuid()
        file_upload.save(os.path.join(constants.FILE_STORE_FOLDER, fuuid))

        new_file = LxFile(fuuid = fuuid, type = 1)
        return {"fid":"000","fname":'+filename+'}
    else:
        return {"fid":"000","errMsg":'error'}

@mod_file.route('/get_url/<fuuid>', methods=['GET'])
def get_url(fuuid):
    """ Get static file url from database
    """


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in constants.ALLOWED_EXTENSIONS

def is_static_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in constants.STITIC_FILE_EXTENSIONS


def generate_file_uuid():
    """ Generate file name use uuid
    May be replace with other generate method
    """
    return uuid.uuid1().hex