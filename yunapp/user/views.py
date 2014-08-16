# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, jsonify, current_app, request
from flask.ext.login import LoginManager, login_required, current_user, login_user, logout_user
from yunapp.yunapps import app
from yunapp.orm import model, engine
from yunapp import config
import hashlib, time
# 下面这两句是发邮件的
import smtplib
from email.mime.text import MIMEText

user = Blueprint('user', __name__)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader  # Flask-login通过这个回调函数加载用户
def load_user(user_id):
    with engine.with_session() as ss:
        current_user = ss.query(model.LxUser).filter_by(id=user_id).first()
    return current_user


@user.route('/<int:uid>', methods=['GET'])
@login_required
def profile(uid):
    return_dict = {'success': True, 'uid': uid}
    return jsonify(return_dict)


@user.route('/register', methods=['POST'])
def register():
    username = request.values['username']
    #realname = request.values['realname']
    #type = request.values['type']
    passwd = hashlib.md5(request.values['password']).hexdigest()
    print passwd
    email = request.values['email']
    #phone = request.values['phone']
    # parentUserId = request.values['parentUserId']
    # companyId = request.values['companyId']
    parent_user_id = 0
    with engine.with_session() as ss:
        new_company = model.LxCompany()
        ss.add(new_company)
        new_user = model.LxUser(username=username,
                                # real_name=realname,
                                # type=type,
                                passwd=passwd,
                                email=email,
                                # phone=phone,
                                parent_user_id=parent_user_id,
                                company=new_company,
                                signId=0)
        ss.add(new_user)
    sent_mail(username, new_user.email)
    return_dict = {'success': True, 'uid': new_user.id}
    return jsonify(return_dict)


@user.route('/active/<activecode>')
@login_required
def user_active(activecode):
    if hashlib.md5(current_user.username+config.MD5_XXXX).hexdigest() == activecode:
        with engine.with_session() as ss:
            current_user.status = 2
        return 'True'
    else:
        return 'False'


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
    username = request.values['username']
    passwd = hashlib.md5(request.values['password']).hexdigest()
    with engine.with_session() as ss:
        luser = ss.query(model.LxUser).filter_by(username=username, passwd=passwd).first()

    if luser:
        return_dict = {'success': True, 'errmsg': '登陆成功' + str(luser.id)}
        login_user(luser)
    else:
        return_dict = {'success': False, 'errmsg': '用户名或密码错误'}
    return jsonify(return_dict)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    pass


@user.route('/test', methods=['POST'])
@login_required
def test():
    return_dict = {'success': False, 'errorMsg': '用户已经登陆啦啦啦' + str(current_user.id)}
    return jsonify(return_dict)


def sent_mail(username, uemail):
    msg = MIMEText(hashlib.md5(username).hexdigest())
    msg['Subject'] = "这是一分激活邮件"
    msg['From'] = "seanwu@yunhetong.net"
    msg['To'] = uemail
    s = smtplib.SMTP('smtp.mailgun.org', 587)
    s.login('postmaster@sandboxc264adea79684d24b0fa4e884e7167de.mailgun.org', '9ef4b057eb214a991e5e24fc1b4814e2')
    s.sendmail(msg['From'], msg['To'], msg.as_string())
    s.quit()