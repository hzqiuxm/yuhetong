# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, jsonify, current_app, request
from flask.ext.login import LoginManager, login_required, current_user, login_user, logout_user
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
        ss.add(new_company)
        new_user = model.LxUser(username=args['username'],
                                # real_name=args['realname'],
                                type=args['type'],
                                passwd=args['passwd'],
                                email=args['email'],
                                # phone=args['phone'],
                                parent_user_id=args['parent_user_id'],
                                company=new_company,
                                signId=args['signId'])
        ss.add(new_user)
    e_content = get_email_content(args['username'])
    if utils.sent_mail(e_content=e_content, e_from='seanwu@yunhetong.net', e_to=new_user.email, e_subject='这是一封激活邮件'):
        return_dict = {'success': True, 'uid': new_user.id}
    else:
        return_dict = {'success': False, 'errmsg': '激活邮箱发送失败'}
    # business_logger.info('new user '+new_user.username+'register,userid='+new_user.id)
    return jsonify(return_dict)


def get_email_content(username):
    e_content = '这是一份激活邮件，不用回，如果下面的超链接无法打开，请将地址复制到地址栏打开<a href=\"http://192.168.1.55:8092/user/active/' + hashlib.md5(
        username + config.MD5_XXXX).hexdigest() + '\">' + 'http://192.168.1.55:8092/user/active/' + hashlib.md5(
        username + config.MD5_XXXX).hexdigest() + '</a>'
    return e_content


def verify_parameter(args):
    re_args = {}
    pattern_email = re.compile(r'^[\w\d]+[\d\w\_\.]+@([\d\w]+)\.([\d\w]+)(?:\.[\d\w]+)?$')  # 邮件的正则
    pattern_username = re.compile(r'^[\w\d]+[\d\w\_\.]+@([\d\w]+)\.([\d\w]+)(?:\.[\d\w]+)?$')  # 用户名的正则，跟邮箱一样
    if not ('username' in args.keys()
            and 'password' in args.keys()
            and 'email' in args.keys()):
        return False
    match_email = pattern_email.match(args['email'])
    match_username = pattern_username.match(args['username'])
    if not match_email:
        return {'success': False, 'errmsg': '邮箱格式错误'}
    if not match_username:
        return {'success': False, 'errmsg': '用户名格式错误'}
    if not args['password']:
        return {'success': False, 'errmsg': '密码不能为空'}
    for k in args.keys():
        re_args[k] = args[k]
    re_args['type'] = '0'
    re_args['parent_user_id'] = 0
    re_args['signId'] = 0
    re_args['passwd'] = hashlib.md5(request.values['password']).hexdigest()
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
        return_dict = {'success': False, 'errorMsg': '激活失败'}
    return jsonify(return_dict)


@user.route('/namecheck', methods=['POST'])
def namecheck():
    username = request.values['username']
    with engine.with_session() as ss:
        luser = ss.query(model.LxUser).filter_by(username=username).first()
    if luser:
        return_dict = {'success': False, 'errorMsg': '用户名已经存在'}
    else:
        return_dict = {'success': True, 'errorMsg': ''}
    return jsonify(return_dict)


@user.route('/login', methods=['POST'])
def login():
    username = request.values.get('username', '')
    passwd = request.values.get('password', '')
    if not username or not passwd:
        return jsonify({'success': False, 'errmsg': constants.ERROR_CODE['EMPTY_USERNAME_OR_PASS']})
    passwd = hashlib.md5(passwd).hexdigest()
    with engine.with_session() as ss:
        luser = ss.query(model.LxUser).filter_by(username=username, passwd=passwd).first()
        if luser:
            return_dict = {'success': True, 'errmsg': '登陆成功' + str(luser.id)}
            business_logger.info('new user ' + str(luser.username) + 'register,userid=' + str(luser.id) + 'is loginning')
            login_user(luser)
        else:
            return_dict = {'success': False, 'errmsg': '用户名或密码错误'}
    return jsonify(return_dict)


@user.route("/logout")
@login_required
def logout():
    business_logger.info('new user ' + current_user.username + 'register,userid=' + str(current_user.id) + 'logout')
    logout_user()
    return_dict = {'success': True, 'errorMsg': 'no'}
    return jsonify(return_dict)


@user.route("/del", methods=['POST'])
# @login_required
def del_user():
    uid = request.values.get('uid', '')
    if not uid:
        return jsonify({'success': False, 'errmsg': 'uid为空'})
    with engine.with_session() as ss:
        c_user = ss.query(model.LxUser).filter_by(id=uid).first()
        if not c_user:
            return jsonify({'success': False, 'errmsg': '不存在该用户'})
        if c_user.parent_user_id == 0:
            c_com = ss.query(model.LxCompany).filter_by(id=c_user.id).first()
            if c_com:
                c_com.status = -1
        c_user.status = -1
    return_dict = {'success': True, 'errorMsg': 'no'}
    business_logger.info('userid=' + str(c_user.id) + 'is deleted')
    return jsonify(return_dict)


@user.route("/update", methods=['POST'])
#@login_required
def update_user():
    uid = request.values.get('uid', '')
    if not uid:
        return jsonify({'success': False, 'errmsg': 'uid为空'})
    with engine.with_session() as ss:
        c_user = ss.query(model.LxUser).filter_by(id=uid).first()
        if not c_user:
            return jsonify({'success': False, 'errmsg': '不存在该用户'})
        c_user.type = request.values.get('type', c_user.type)
        # username= request.values.get('username',c_user.username)  用户名不给改
        c_user.real_name = request.values.get('real_name', c_user.real_name)
        # c_user.email = request.values.get('email', c_user.email)
        c_user.phone = request.values.get('phone', c_user.phone)
        c_user.modify_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    return_dict = {'success': True, 'errorMsg': 'no'}
    business_logger.info('userid=' + str(c_user.id) + 'has been update')
    return jsonify(return_dict)


@user.route('/test', methods=['POST'])
@login_required
def test():
    return_dict = {'success': False, 'errorMsg': '用户已经登' + str(current_user.id)}
    return jsonify(return_dict)


