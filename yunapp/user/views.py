# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, jsonify, current_app, request
from flask.ext.login import LoginManager, login_required, current_user, login_user
from yunapp.yunapps import app
from yunapp.orm import model, engine
import hashlib, time

user = Blueprint('user', __name__)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader  # Flask-login通过这个回调函数加载用户
def load_user(user_id):
    with engine.with_session() as ss:
        current_user = ss.query(model.LxUser).filter_by(id=user_id).first()
    return current_user


@user.route('/<int:uid>', methods=['GET'])
def profile(uid):
    return_dict = {'success': True, 'uid': uid}
    return jsonify(return_dict)


@user.route('/register', methods=['POST'])
def register():
    userName = request.values['username']
    realName = request.values['realName']
    type = request.values['type']
    passwd = hashlib.md5(request.values['passwd']).hexdigest()
    print passwd
    email = request.values['email']
    phone = request.values['phone']
    # parentUserId = request.values['parentUserId']
    # companyId = request.values['companyId']
    companyId = 1
    parentUserId = 0
    with engine.with_session() as ss:
        new_user = model.LxUser(userName=userName,
                                realName=realName,
                                type=type,
                                passwd=passwd,
                                email=email,
                                phone=phone,
                                parentUserId=parentUserId,
                                companyId=companyId,
                                signId=0)
        ss.add(new_user)
    return_dict = {'success': True, 'uid': new_user.id}
    return jsonify(return_dict)


@user.route('/namecheck', methods=['POST'])
def namecheck():
    userName = request.values['username']
    with engine.with_session() as ss:
        luser = ss.query(model.LxUser).filter_by(userName=userName).first()
    if luser:
        return_dict = {'success': False, 'errorMsg': '用户名已经存在'}
    else:
        return_dict = {'success': True, 'errorMsg': ''}
    return jsonify(return_dict)


@user.route('/login', methods=['POST'])
def login():
    userName = request.values['username']
    passwd = hashlib.md5(request.values['passwd']).hexdigest()
    with engine.with_session() as ss:
        luser = ss.query(model.LxUser).filter_by(userName=userName, passwd=passwd).first()

    if luser:
        return_dict = {'success': True, 'errorMsg': '登陆成功' + str(luser.id)}
        login_user(luser)
    else:
        return_dict = {'success': False, 'errorMsg': '用户名或密码错误'}
    return jsonify(return_dict)


@app.route("/logout")
@login_required
def logout():
    # logout_user()
    pass


@user.route('/test', methods=['POST'])
@login_required
def test():
    return_dict = {'success': False, 'errorMsg': '用户已经登陆啦啦啦' + str(current_user.id)}
    return jsonify(return_dict)
