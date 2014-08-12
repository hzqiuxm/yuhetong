# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, jsonify, current_app, request
from flask.ext.login import LoginManager
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import User
from yunapp.yunapps import app

from yunapp import config
import hashlib, time

user = Blueprint('user', __name__)
engine = create_engine(config.DATABASE_URI, convert_unicode=True)
# 创建了一个自定义了的 Session类
Session = sessionmaker()
# 将创建的数据库连接关联到这个session
Session.configure(bind=engine)
session = Session()

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    query = session.query(User)
    return query.filter_by(uid=user_id).limit(1)


@user.route('/<int:uid>', methods=['GET'])
def profile(uid):
    return_dict = {'success': True, 'uid': uid}
    return jsonify(return_dict)

@user.route('/register', methods=['POST'])
def register():

    username = request.values['username']
    realName = request.values['realName']
    type = request.values['type']
    passwd = hashlib.md5(request.values['passwd'])
    email = request.values['email']
    phone = request.values['phone']
    parentUserId = request.values['parentUserId']
    companyId = request.values['companyId']

    u = User(username=username,
             realName=realName,
             type=type,
             passwd=passwd,
             email=email,
             phone=phone,
             parentUserId=parentUserId,
             companyId=companyId,
             signId=0)
    return_dict = {'success': True, 'uid': 'uid'}
    return jsonify(return_dict)

    with engine.with_session() as ss:
        new_user = model.User(type=1, userName='test', realName='testreal',
                              passwd='pass', email='xudabin@yunhetong.net',
                              status=0 )
        ss.add(new_user)
        return_dict = {'success': True, 'uid':'uid'}
        return jsonify(return_dict)



@user.route('/namecheck')
def namecheck():
    return_dict = {'success': True, 'errorMsg': ''}
    return jsonify(return_dict)


@user.route('/login', methods=['POST'])
def login():
    return_dict = {'success': True, 'errorMsg': 'no'}
    return jsonify(return_dict)