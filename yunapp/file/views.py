# -*- coding: utf-8 -*-
import os, uuid, logging
from flask import Blueprint, render_template, jsonify, request, send_file
import constants
from yunapp.orm import model
from yunapp.orm import engine
from yunapp.logutils import StructedMsg

mod_file = Blueprint('file', __name__)
app_logger = logging.getLogger('yunapp')
biz_logger = logging.getLogger('business')

@mod_file.route('/upload', methods=['POST'])
def upload():
    """ Upload file
    upload from user and store on server
    """
    file_upload = request.files['user_file']
    file_name = request.args.get('user_file_name')
    if not file_name:
        file_name = 'empty_name'
    if file_upload and allowed_file(file_upload.filename):
        file_extention = file_upload.filename.rsplit('.', 1)[1]
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
        return jsonify({'fid':new_file.id, 'fname': file_name})
    else:
        return jsonify({'fid':'','errMsg': constants.ERROR_CODE[
            'NOT_ALLOWED_FILE']})

@mod_file.route('/get_static_file/<fuuid>', methods=['GET'])
def get_static_file(fuuid):
    """ Get static file url from database
    """
    if has_perm('user', 'fuuid'):
        with engine.with_session() as ss:
            static_file = ss.query(model.LxFile).filter_by(fuuid =
                                                           fuuid).first()
            return send_file(static_file.fpath, mimetype='image/' +
                                                         static_file.extension)
    else:
        return jsonify({'fuuid':fuuid,'errMsg': constants.ERROR_CODE[
            'NO_PERM_FOR_FILE']})


# TODO(wenwu) get_contract should in contract model
@mod_file.route('/get_contract/<cid>', methods=['GET'])
def get_contract(cid):
    """ Get static file url from database
    """
    if has_contract_perm('user', 'fuuid'):
        with engine.with_session() as ss:
            pass
    else:
        return jsonify({'cid':cid,'errMsg': constants.ERROR_CODE[
            'NO_PERM_FOR_CONTRACT']})

def has_contract_perm(user_id, fuuid):
    return True
# TODO_END

# TODO(wenwu) test code for logging
@mod_file.route('/testlog', methods=['GET'])
def test_log():
    app_logger.info(StructedMsg("log msg", model=__name__))
    return jsonify({'fid':'xxx'})

@mod_file.route('/testlogbusiness', methods=['GET'])
def test_business_log():
    biz_logger.info('business')
    return jsonify({'fid':'xxx'})
# TODO_END

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

# TODO(wenwu) check perm
def has_perm(user_id, fuuid):
    return True
# TODO_END

@mod_file.route('/file_html')
def file_list():
    return render_template('file.html')