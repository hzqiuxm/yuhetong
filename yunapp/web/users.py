# -*- coding: utf-8 -*-
import hashlib
from flask import Blueprint,render_template ,jsonify
from flask.ext.login import LoginManager, login_required, current_user, login_user, logout_user

web_users = Blueprint('web_users', __name__)


# TODO Delete when get online
@web_users.route('/test', methods=['POST'])
@login_required
def test():
    return_dict = {'success': False, 'errorMsg': '用户已经登' + str(current_user.id)}
    return jsonify(return_dict)


@web_users.route('/login', methods=['GET'])
def login_page():
    if current_user.is_authenticated():
        # return render_template('user/login.html')
        return render_template('newhome.html')
    else:
        return render_template('user/login.html')

@web_users.route('/authentication', methods=['GET'])
def smrz_page():
    return render_template('user/certification.html')

@web_users.route('/resetpwd/<resetcode>',methods=['GET'])
def load_reset_password_page(resetcode):
    if hashlib.md5(current_user.username + config.MD5_XXXX).hexdigest() == resetcode:
        current_user.password = 2
        business_logger.info('user\'s password has been reset,userid=' + str(current_user.id))
        return_dict = {'success': True, 'errorMsg': '修改密码成功'}
    else:
        return_dict = {'success': False, 'errorMsg': constants.ERROR_CODE['RESERT_CODE_ERROR']}
    return jsonify(return_dict)