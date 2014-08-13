# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, jsonify, current_app, request
from flask.ext.login import LoginManager
from yunapp.yunapps import app
from yunapp.orm import model, engine
import hashlib, time

user = Blueprint('user', __name__)

login_manager = LoginManager()
login_manager.init_app(app)


# @login_manager.user_loader
# def load_user(user_id):
# query = session.query(User)
#     return query.filter_by(uid=user_id).limit(1)


@user.route('/<int:uid>', methods=['GET'])
def profile(uid):
    return_dict = {'success': True, 'uid': uid}
    return jsonify(return_dict)


@user.route('/register', methods=['POST'])
def register():
    print 'xxx'
    username = request.values['username']
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
        new_user = model.LxUser(userName=username,
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


@user.route('/namecheck')
def namecheck():
    return_dict = {'success': True, 'errorMsg': ''}
    return jsonify(return_dict)


@user.route('/login', methods=['POST'])
def login():
    return_dict = {'success': True, 'errorMsg': 'no'}
    return jsonify(return_dict)