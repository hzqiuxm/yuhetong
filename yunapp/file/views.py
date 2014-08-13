# -*- coding: utf-8 -*-
import os, uuid
from flask import Blueprint, render_template, jsonify, request, config
import constants
from yunapp.orm import model
from yunapp.orm import engine
mod_file = Blueprint('file', __name__)

@mod_file.route('/upload', methods=['POST'])
def upload():
    """ Upload file
    upload from user and store on server
    """
    file_upload = request.files['userfile']
    print file_upload
    file_name = request.args.get('user_file_name')
    if not file_name:
        file_name = 'empty'
    if file_upload and allowed_file(file_upload.filename):
        file_extention = file_upload.filename.rsplit('.', 1)[1]
        print file_extention
        file_type = get_file_type(file_extention)

        fuuid = generate_file_uuid()
        file_path = save_file(file_upload, fuuid)

        with engine.with_session() as ss:
            new_file = model.LxFile(fuuid = fuuid,
                                    type = file_type,
                                    name = file_name,
                                    fpath = file_path,
                                    extension = file_extention)
            ss.add(new_file)
        return jsonify({'fid':new_file.id})
    else:
        return jsonify({'fid':'','errMsg': constants.ERROR_CODE[
            'NOT_ALLOWED_FILE']})

@mod_file.route('/get_url/<fuuid>', methods=['GET'])
def get_url(fuuid):
    """ Get static file url from database
    """

def is_contract():
    """ Check file is contract or not
    """
    return False

def allowed_file(filename):
    """ Check file is allowed by the system
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in constants.ALLOWED_EXTENSIONS

def generate_file_uuid():
    """ Generate file name use uuid
    May be replace with other generate method
    """
    return uuid.uuid1().hex

def save_file(file_upload, fuuid):
    """ Save file and return file path
    Currently use local file
    """
    try:
        file_path = os.path.join(constants.FILE_STORE_FOLDER, fuuid)
        file_upload.save(file_path)
        return file_path
    except:
        return None

def get_file_type(file_extention):
    """ Get file type from extention or
    1 means contract, 2 means static file, 3 means others
    """
    if is_contract():
        file_type = 1
    elif file_extention in constants.STITIC_FILE_EXTENSIONS:
        file_type = 2
    else:
        file_type = 3
    return file_type