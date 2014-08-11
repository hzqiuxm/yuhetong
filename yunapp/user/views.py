# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, jsonify
import flask.ext.login.LoginManager as LoginManager
from models import User
login_manager = LoginManager()

user = Blueprint('user', __name__)
login_manager.init_app(user)


@login_manager.user_loader
def load_user(userid):
    return User.get(userid)

@user.route('/register', methods=['POST'])
def register():

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