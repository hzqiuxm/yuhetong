# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, jsonify, current_app, request
from flask.ext.login import LoginManager, login_required, current_user, login_user, logout_user
from flask.ext.bcrypt import Bcrypt
from yunapp.yunapps import app
from yunapp.orm import model, engine
from yunapp import config
import hashlib, time, re, logging
from yunapp import utils
from yunapp.user import constants
from yunapp.logutils import StructedMsg


user = Blueprint('user', __name__)
app_logger = logging.getLogger('yunapp')
business_logger = logging.getLogger('business')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"
# login_manager.login_view = "users.login"

bcrypt = Bcrypt(app)


@login_manager.user_loader  # Flask-login通过这个回调函数加载用户
def load_user(user_id):
    with engine.with_session() as ss:
        c_user = ss.query(model.LxUser).filter_by(id=user_id).first()
    return c_user


@user.route('/<int:uid>', methods=['GET'])
@login_required
def profile(uid):
    return_dict = {'success': True, 'uid': uid}
    return jsonify(return_dict)


@user.route('/register', methods=['POST'])
def register():
    args = verify_parameter(request.values)
    if 'success' in args:
        return jsonify(args)
    with engine.with_session() as ss:
        new_company = model.LxCompany()
        new_company.name = time.time()
        ss.add(new_company)
        new_user = model.LxUser(username=args['username'],
                                # real_name=args['realname'],
                                type=args['type'],
                                passwd=args['password'],
                                email=args['email'],
                                # phone=args['phone'],
                                # parent_id=args['parent_user_id'],
                                company=new_company)
        ss.add(new_user)
    e_content = get_email_content(args['username'])
    if utils.sent_mail(e_content=e_content, e_from='seanwu@yunhetong.net', e_to=new_user.email, e_subject='这是一封激活邮件'):
        return_dict = {'success': True, 'uid': new_user.id}
        login_user(new_user)
    else:
        return_dict = {'success': False, 'errmsg': constants.ERROR_CODE['SENT_ACCTIVE_EMAIL_ERROR']}
    # business_logger.info('new user '+new_user.username+'register,userid='+new_user.id)
    return jsonify(return_dict)


def get_email_content(username):
    active_code =hashlib.md5( username + config.MD5_XXXX).hexdigest()
    e_content = '这是一份激活邮件，不用回，如果下面的超链接无法打开，请将地址复制到地址栏打开<a href=\"http://192.168.1.55:8092/user/active/' + active_code+ '\">' + 'http://192.168.1.55:8092/user/active/' + active_code+ '</a>'
    return e_content


def verify_parameter(args):
    re_args = {}
    pattern_email = re.compile(r'^[\w\d]+[\d\w\_\.]+@([\d\w]+)\.([\d\w]+)(?:\.[\d\w]+)?$')  # 邮件的正则
    pattern_username = re.compile(r'^[\w\d]+[\d\w\_\.]+@([\d\w]+)\.([\d\w]+)(?:\.[\d\w]+)?$')  # 用户名的正则，跟邮箱一样
    if not ('username' in args.keys()
            and 'password' in args.keys()
            and 'email' in args.keys()):
        return {'success': False, 'errmsg': constants.ERROR_CODE['EMAIL_FORMAT_ERROR']}
    match_email = pattern_email.match(args['email'])
    match_username = pattern_username.match(args['username'])
    if not match_email:
        return {'success': False, 'errmsg': constants.ERROR_CODE['EMAIL_FORMAT_ERROR']}
    if not match_username:
        return {'success': False, 'errmsg': constants.ERROR_CODE['USER_FORMAT_ERROR']}
    if not args['password']:
        return {'success': False, 'errmsg': constants.ERROR_CODE['PASSWORD_NULL_ERROR']}
    for k in args.keys():
        re_args[k] = args[k]
    re_args['type'] = '0'
    re_args['parent_user_id'] = 0
    re_args['signId'] = 0
    # re_args['password'] = hashlib.md5(request.values['password']).hexdigest()
    re_args['password'] = bcrypt.generate_password_hash(request.values['password'])
    return re_args


@user.route('/active/<activecode>', methods=['POST'])
@login_required
def user_active(activecode):
    if hashlib.md5(current_user.username + config.MD5_XXXX).hexdigest() == activecode:
        with engine.with_session() as ss:
            current_user.status = 2
        business_logger.info(
            'user ' + current_user.username + 'register,userid=' + str(current_user.id) + 'atcive success')
        return_dict = {'success': True, 'errorMsg': '用户已经成功激活'}
    else:
        return_dict = {'success': False, 'errorMsg': constants.ERROR_CODE['ACTIVE_FAILD']}
    return jsonify(return_dict)


@user.route('/namecheck', methods=['POST'])
def namecheck():
    username = request.values['username']
    with engine.with_session() as ss:
        luser = ss.query(model.LxUser).filter_by(username=username).first()
    if luser:
        return_dict = {'success': False, 'errorMsg': constants.ERROR_CODE['USERNAME_EXISTS_ERROR']}
    else:
        return_dict = {'success': True, 'errorMsg': ''}
    return jsonify(return_dict)


@user.route('/login', methods=['POST'])
def login():
    username = request.values.get('username', '')
    passwd = request.values.get('password', '')
    if not username or not passwd:
        return jsonify({'success': False, 'errmsg': constants.ERROR_CODE['EMPTY_USERNAME_OR_PASS']})
    with engine.with_session() as ss:
        luser = ss.query(model.LxUser).filter_by(username=username).first()
        if luser:
            if bcrypt.check_password_hash(luser.passwd, passwd):
                return_dict = {'success': True, 'errmsg': '登陆成功', 'uid': str(luser.id)}
                business_logger.info(
                    'user ' + str(luser.username) + 'login,userid=' + str(luser.id) + 'is loginning')
                login_user(luser)
            else:
                return_dict = {'success': False, 'errmsg': constants.ERROR_CODE[
                    'PASS_ERROR']}
        else:
            return_dict = {'success': False, 'errmsg': constants.ERROR_CODE[
                'USERNAME_NOT_EXISTS_ERROR']}
    return jsonify(return_dict)


@user.route("/logout")
# @login_required
def logout():
    business_logger.info('user' + current_user.username + ',userid=' + str(current_user.id) + 'logout')
    logout_user()
    return_dict = {'success': True, 'errorMsg': 'no'}
    return jsonify(return_dict)


@user.route("/del", methods=['DELETE'])
# @login_required
def del_user():
    uid = request.values.get('uid', '')
    password = request.values.get('password', '')
    if not uid:
        return jsonify({'success': False, 'errmsg': constants.ERROR_CODE['UID_EMPTY_ERROR']})
    with engine.with_session() as ss:
        c_user = ss.query(model.LxUser).filter_by(id=uid).first()
        if not c_user:
            return jsonify({'success': False, 'errmsg': constants.ERROR_CODE['USERNAME_NOT_EXISTS_ERROR']})
        elif not bcrypt.check_password_hash(c_user.passwd, password):
            return jsonify({'success': False, 'errmsg': constants.ERROR_CODE['PASS_ERROR']})
        if c_user.parent_id == 0:
            c_com = ss.query(model.LxCompany).filter_by(id=c_user.id).first()
            if c_com:
                c_com.status = -1
        c_user.status = -1
    return_dict = {'success': True, 'errorMsg': 'no'}
    business_logger.info('userid=' + str(c_user.id) + 'is deleted')
    return jsonify(return_dict)


@user.route("/update", methods=['PUT'])
# @login_required
def update_user():
    uid = request.values.get('uid', '')
    password = request.values.get('password', '')
    if not uid:
        return jsonify({'success': False, 'errmsg': 'uid为空'})
    with engine.with_session() as ss:
        c_user = ss.query(model.LxUser).filter_by(id=uid).first()
        if not c_user:
            return jsonify({'success': False, 'errmsg': constants.ERROR_CODE['USERNAME_NOT_EXISTS_ERROR']})
        elif not bcrypt.check_password_hash(c_user.passwd, password):
            return jsonify({'success': False, 'errmsg': constants.ERROR_CODE['PASS_ERROR']})
        c_user.type = request.values.get('type', c_user.type)
        # username= request.values.get('username',c_user.username)  用户名不给改
        c_user.real_name = request.values.get('real_name', c_user.real_name)
        # c_user.email = request.values.get('email', c_user.email)
        c_user.phone = request.values.get('phone', c_user.phone)
        c_user.modify_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    return_dict = {'success': True, 'errorMsg': 'no'}
    business_logger.info('userid=' + str(c_user.id) + 'has been update')
    return jsonify(return_dict)


@user.route("/resetpwd", methods=['PUT'])
# @login_required
def resert_password():
    uid = request.values.get('uid', '')
    password = request.values.get('password', '')
    if not uid:
        return jsonify({'success': False, 'errmsg': 'uid为空'})
    with engine.with_session() as ss:
        c_user = ss.query(model.LxUser).filter_by(id=uid).first()
        if not c_user:
            return jsonify({'success': False, 'errmsg': constants.ERROR_CODE['USERNAME_NOT_EXISTS_ERROR']})
        elif not bcrypt.check_password_hash(c_user.passwd, password):
            return jsonify({'success': False, 'errmsg': constants.ERROR_CODE['PASS_ERROR']})

    return_dict = {'success': True, 'errorMsg': 'no'}
    business_logger.info('userid=' + str(c_user.id) + 'has been update')
    return jsonify(return_dict)

@user.route("/authenticationuser", methods=['PUT'])
# @login_required
def renzheng_user():
    with engine.with_session() as ss:
        # username= request.values.get('username',c_user.username)  用户名不给改
        current_user.real_name = request.values.get('real_name', current_user.real_name)
        # c_user.email = request.values.get('email', c_user.email)
        current_user.phone = request.values.get('phone', current_user.phone)
        current_user.idCardNo = request.values.get('idCardNo', current_user.idCardNo)
        current_user.idCardimg1 = request.values.get('idCardimg1', current_user.idCardimg1)
        current_user.idCardimg2 = request.values.get('idCardimg2', current_user.idCardimg2)
        current_user.authorization_img = request.values.get('authorizationimg', current_user.authorization_img)
        current_user.address = request.values.get('address', current_user.phone)
        current_user.modify_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    return_dict = {'success': True, 'errorMsg': 'no'}
    business_logger.info('userid=' + str(current_user.id) + 'has been update')
    return jsonify(return_dict)


@user.route("/authenticationcompany", methods=['PUT'])
# @login_required
def renzheng_company():
    with engine.with_session() as ss:
        c_com = ss.query(model.LxCompany).filter_by(id=current_user.id).first()
        c_com.name = request.values.get('name', c_com.name)
        c_com.organizationNo = request.values.get('organizationNo', c_com.organizationNo)
        c_com.organization_img = request.values.get('organizationimg', c_com.organization_img)
        c_com.business_license_No = request.values.get('business_license_No', c_com.business_license_No)
        c_com.business_license_img = request.values.get('business_license_img', c_com.business_license_img)
        c_com.legal_person = request.values.get('legal_person', c_com.legal_person)
        c_com.address = request.values.get('address', c_com.address)
    return_dict = {'success': True, 'errorMsg': 'no'}
    business_logger.info('userid=' + str(current_user.id) + 'has been update')
    return jsonify(return_dict)



