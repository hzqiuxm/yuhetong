# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, jsonify, current_app
from flask.ext.login import LoginManager
from models import User
from yunapp.yunapps import app
from yunapp.orm import engine, model

login_manager = LoginManager()
login_manager.init_app(app)

user = Blueprint('user', __name__)

@login_manager.user_loader
def load_user(userid):
    return User.get(userid)


@user.route('/<int:uid>', methods=['GET'])
def profile(uid):
    return_dict = {'success': True, 'uid':uid}
    return jsonify(return_dict)

@user.route('/register', methods=['POST', 'GET'])
def register():
    with engine.with_session() as ss:
        new_user = model.User()
        ss.add(new_user)
        return_dict = {'success': True, 'uid':'uid'}
        return jsonify(return_dict)


@user.route('/namecheck')
def namecheck():
    return_dict = {'success': True, 'errorMsg':''}
    return jsonify(return_dict)


@user.route('/login')
def login():
    return_dict = {'success': True, 'errorMsg':''}
    return jsonify(return_dict)